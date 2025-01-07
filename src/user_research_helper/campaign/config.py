import os
import json
from typing import Dict, Any, Optional

class Config:
    _instance = None
    _config = None
    _root_dir = None
    _initialized = False

    # Project file structure configuration
    PROJECT_PATHS = {
        'question_file': 'questions.txt',
        'audio_dir': 'audios',
        'raw_transcript_dir': 'transcripts/raw',
        'structured_transcript_dir': 'transcripts/structured',
        'transcript_report_dir': 'transcripts',
        'analysis_dir': 'analysis',
        'segment_analysis_dir': 'analysis/segments',
        'config_file': 'config.json'
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the singleton instance"""
        if not hasattr(self, '_initialized'):
            self._initialized = False

    def initialize(self, root_dir: str) -> None:
        """
        Initialize the configuration with the root directory.
        This must be called before using any other methods.
        
        Args:
            root_dir: Root directory for the project
            
        Raises:
            ValueError: If root_dir is None or empty
            FileNotFoundError: If root_dir doesn't exist
        """
        if not root_dir:
            raise ValueError("root_dir cannot be None or empty")
            
        if not os.path.isdir(root_dir):
            raise FileNotFoundError(f"root_dir does not exist: {root_dir}")
            
        self._root_dir = os.path.abspath(root_dir)
        self._load_config()
        self._initialized = True

    def _check_initialized(self) -> None:
        """
        Check if the configuration has been initialized
        
        Raises:
            RuntimeError: If initialize() hasn't been called
        """
        if not self._initialized:
            raise RuntimeError(
                "Config not initialized. You must call initialize(root_dir) "
                "before using any configuration methods."
            )

    def _load_config(self) -> None:
        """
        Load configuration from JSON file
        
        Raises:
            FileNotFoundError: If config file doesn't exist
            json.JSONDecodeError: If config file is invalid JSON
        """
        config_path = os.path.join(self._root_dir, self.PROJECT_PATHS['config_file'])
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f"Configuration file not found at: {config_path}\n"
                f"Please ensure {self.PROJECT_PATHS['config_file']} exists in the root directory."
            )
            
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in configuration file: {str(e)}\n"
                f"Please check the format of {config_path}",
                e.doc, e.pos
            )

    def get_path(self, path_key: str) -> str:
        """
        Get absolute path for a project component
        
        Args:
            path_key: Key from PROJECT_PATHS
            
        Returns:
            str: Absolute path
            
        Raises:
            KeyError: If path_key is not in PROJECT_PATHS
        """
        self._check_initialized()
        
        if path_key not in self.PROJECT_PATHS:
            raise KeyError(f"Unknown path key: {path_key}")
        
        return os.path.join(self._root_dir, self.PROJECT_PATHS[path_key])

    def get_config(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value
        
        Args:
            key: Configuration key (supports dot notation for nested access)
            default: Default value if key not found
            
        Returns:
            Any: Configuration value
        """
        self._check_initialized()
        
        # Handle nested keys (e.g., "llm_context.transcript_analysis.temperature")
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    @property
    def root_dir(self) -> str:
        """
        Get the root directory
        
        Returns:
            str: Absolute path to root directory
            
        Raises:
            RuntimeError: If initialize() hasn't been called
        """
        self._check_initialized()
        return self._root_dir

    @property
    def language(self) -> str:
        """Get the configured language"""
        self._check_initialized()
        return self.get_config('language', 'fr')

    @property
    def word_boost(self) -> list:
        """Get the word boost list"""
        self._check_initialized()
        return self.get_config('word_boost', [])

    @property
    def llm_context(self) -> dict:
        """Get the LLM context configuration"""
        self._check_initialized()
        return self.get_config('llm_context', {})

    @property
    def debug(self) -> dict:
        """
        Get debug settings
        
        Returns:
            dict: Debug configuration with keys:
                - print_questions: bool
                - print_transcripts: bool
                - print_analysis: bool
                - verbose: bool
        """
        self._check_initialized()
        return self.get_config('debug', {
            'print_questions': False,
            'print_transcripts': False,
            'print_analysis': False,
            'verbose': False
        })

    def should_debug(self, key: str) -> bool:
        """
        Check if a specific debug feature is enabled
        
        Args:
            key: Debug key to check (e.g., 'print_questions', 'verbose')
            
        Returns:
            bool: Whether the debug feature is enabled
        """
        return self.debug.get(key, False)

# Global instance
config = Config()
