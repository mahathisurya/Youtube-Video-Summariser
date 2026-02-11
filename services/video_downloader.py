"""
YouTube video download and audio extraction service
"""
import os
import logging
import yt_dlp
from moviepy.editor import VideoFileClip, AudioFileClip
from typing import Tuple, Dict
from utils.error_handlers import VideoDownloadError, retry_on_failure

logger = logging.getLogger(__name__)

class VideoDownloader:
    """Handles YouTube video download and audio extraction"""
    
    def __init__(self, temp_dir: str = "temp_videos"):
        self.temp_dir = temp_dir
        self.audio_dir = "temp_audio"
        
        # Create directories if they don't exist
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.audio_dir, exist_ok=True)
    
    @retry_on_failure(max_retries=3, delay=2.0)
    def download_video(self, video_url: str, video_id: str) -> Tuple[str, Dict]:
        """
        Download YouTube video and extract audio
        
        Args:
            video_url: YouTube video URL
            video_id: Video ID
            
        Returns:
            Tuple of (audio_file_path, video_metadata)
        """
        try:
            logger.info(f"Downloading video: {video_url}")
            
            # Configure yt-dlp options
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(self.audio_dir, f'{video_id}.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            
            # Download video info first to check duration
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(video_url, download=False)
                
                # Validate video duration (max 2 hours by default)
                max_duration = int(os.getenv('MAX_VIDEO_DURATION', 7200))
                duration = info.get('duration', 0)
                
                if duration > max_duration:
                    raise VideoDownloadError(
                        f"Video duration ({duration}s) exceeds maximum allowed ({max_duration}s)"
                    )
                
                # Get video metadata
                metadata = {
                    'title': info.get('title', 'Unknown'),
                    'author': info.get('uploader', 'Unknown'),
                    'duration': duration,
                    'views': info.get('view_count', 0),
                    'thumbnail': info.get('thumbnail', ''),
                    'description': (info.get('description', '') or '')[:500]
                }
                
                logger.info(f"Video metadata: {metadata['title']} - {metadata['duration']}s")
            
            # Download audio
            logger.info("Downloading audio stream...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            
            # Find the downloaded audio file
            audio_path = os.path.join(self.audio_dir, f"{video_id}.mp3")
            
            if not os.path.exists(audio_path):
                # Try other possible extensions
                for ext in ['m4a', 'webm', 'opus']:
                    alt_path = os.path.join(self.audio_dir, f"{video_id}.{ext}")
                    if os.path.exists(alt_path):
                        audio_path = alt_path
                        break
            
            if not os.path.exists(audio_path):
                raise VideoDownloadError("Audio file not found after download")
            
            # Convert to WAV for better compatibility with transcription services
            wav_path = self._convert_to_wav(audio_path, video_id)
            
            # Clean up original audio file
            if os.path.exists(audio_path) and audio_path != wav_path:
                os.remove(audio_path)
            
            logger.info(f"Audio extraction complete: {wav_path}")
            return wav_path, metadata
            
        except yt_dlp.utils.DownloadError as e:
            logger.error(f"yt-dlp download error: {str(e)}")
            raise VideoDownloadError(f"Failed to download video: {str(e)}")
        except Exception as e:
            logger.error(f"Download error: {str(e)}")
            raise VideoDownloadError(f"Error during video download: {str(e)}")
    
    def _convert_to_wav(self, audio_path: str, video_id: str) -> str:
        """
        Convert audio file to WAV format
        
        Args:
            audio_path: Path to audio file
            video_id: Video ID
            
        Returns:
            Path to WAV file
        """
        try:
            wav_path = os.path.join(self.audio_dir, f"{video_id}.wav")
            
            # Load audio and convert
            logger.info("Converting audio to WAV format...")
            try:
                # Try loading as audio file first
                audio_clip = AudioFileClip(audio_path)
            except:
                # If that fails, try loading as video file
                audio_clip = VideoFileClip(audio_path).audio
            
            audio_clip.write_audiofile(wav_path, codec='pcm_s16le', logger=None)
            audio_clip.close()
            
            return wav_path
        except Exception as e:
            logger.error(f"Audio conversion error: {str(e)}")
            # If conversion fails, return original file (AssemblyAI can handle mp3)
            logger.info("Using original audio file format")
            return audio_path
    
    def cleanup(self, file_path: str):
        """
        Clean up temporary files
        
        Args:
            file_path: Path to file to delete
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup file {file_path}: {str(e)}")
    
    def cleanup_all(self):
        """Clean up all temporary files"""
        for directory in [self.temp_dir, self.audio_dir]:
            try:
                if os.path.exists(directory):
                    for file in os.listdir(directory):
                        file_path = os.path.join(directory, file)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    logger.info(f"Cleaned up directory: {directory}")
            except Exception as e:
                logger.warning(f"Failed to cleanup directory {directory}: {str(e)}")
