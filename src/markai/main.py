#!/usr/bin/env python3
"""
MarkAI - Advanced AI Assistant
Main Application Module

A sophisticated AI assistant with advanced cognitive capabilities including:
- Multi-type reasoning (analytical, creative, strategic, ethical)
- Advanced memory networks with episodic & semantic memory
- Chain-of-thought reasoning with meta-cognition
- Multi-modal processing (text, images, documents)
- Enterprise-grade plugin ecosystem
- Real-time cognitive state monitoring
- Adaptive learning and personalization
"""

import asyncio
import argparse
import sys
from pathlib import Path

# Import MarkAI modules
from .core.advanced_ai_engine import AdvancedMarkAICore, ProcessingMode, ReasoningType
from .cli.advanced_interface import AdvancedCLIInterface  
from .api.advanced_server import AdvancedWebInterface
from .utils.config import Config
from .utils.logger import get_logger, setup_logging


async def start_cli_interface(config_path: str, **kwargs):
    """Start the advanced CLI interface"""
    try:
        # Load configuration
        config = Config(config_path)
        
        # Initialize advanced AI engine
        ai_engine = AdvancedMarkAICore(config)
        
        # Create and start CLI interface
        cli = AdvancedCLIInterface(ai_engine, config)
        
        # Set initial modes from kwargs
        if 'processing_mode' in kwargs:
            cli.current_mode = ProcessingMode(kwargs['processing_mode'])
        if 'reasoning_type' in kwargs:
            cli.current_reasoning = ReasoningType(kwargs['reasoning_type'])
        if 'monitor' in kwargs:
            cli.monitoring_enabled = kwargs['monitor']
        
        await cli.start()
        
    except Exception as e:
        logger = get_logger(__name__)
        logger.error(f"Error starting CLI: {e}")
        print(f"Error starting CLI: {e}")
        return 1


async def start_web_interface(config_path: str, **kwargs):
    """Start the advanced web interface"""
    try:
        # Load configuration
        config = Config(config_path)
        
        # Create and start web interface
        web_interface = AdvancedWebInterface(config)
        
        # Get host and port from kwargs or config
        host = kwargs.get('host', config.get('web_interface.host', '127.0.0.1'))
        port = kwargs.get('port', config.get('web_interface.port', 8000))
        
        await web_interface.start_server(host, port)
        
    except Exception as e:
        logger = get_logger(__name__)
        logger.error(f"Error starting web interface: {e}")
        print(f"Error starting web interface: {e}")
        return 1


def show_banner():
    """Show MarkAI banner"""
    banner = """
    ███╗   ███╗ █████╗ ██████╗ ██╗  ██╗ █████╗ ██╗
    ████╗ ████║██╔══██╗██╔══██╗██║ ██╔╝██╔══██╗██║
    ██╔████╔██║███████║██████╔╝█████╔╝ ███████║██║
    ██║╚██╔╝██║██╔══██║██╔══██╗██╔═██╗ ██╔══██║██║
    ██║ ╚═╝ ██║██║  ██║██║  ██║██║  ██╗██║  ██║██║
    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝
    
    🧠 Advanced AI Assistant with Cognitive Intelligence
    
    Features:
    • Multi-type reasoning (analytical, creative, strategic, ethical)
    • Advanced memory networks with episodic & semantic memory  
    • Chain-of-thought reasoning with meta-cognition
    • Multi-modal processing (text, images, documents)
    • Enterprise-grade plugin ecosystem
    • Real-time cognitive state monitoring
    • Adaptive learning and personalization
    """
    print(banner)


def setup_directories():
    """Create necessary directories"""
    directories = ['data', 'logs', 'exports', 'static', 'templates']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="MarkAI - Advanced AI Assistant with Cognitive Intelligence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py cli                           # Start CLI with default settings
  python main.py cli --mode deep --monitor    # Start CLI with deep processing and monitoring
  python main.py web --host 0.0.0.0 --port 8080  # Start web server on all interfaces
  python main.py --banner                     # Show banner and capabilities
  
Interfaces:
  cli    - Advanced command-line interface with rich formatting
  web    - Modern web interface with real-time features
  
Advanced Features:
  • Multi-modal AI processing (text, images, documents)
  • Enterprise plugin ecosystem  
  • Real-time cognitive monitoring
  • Conversation analytics and export
  • Advanced reasoning capabilities
        """
    )
    
    # Add subcommands
    subparsers = parser.add_subparsers(dest='interface', help='Interface to start')
    
    # CLI interface options
    cli_parser = subparsers.add_parser('cli', help='Start advanced CLI interface')
    cli_parser.add_argument('--config', default='config/advanced_config.json', 
                           help='Configuration file path')
    cli_parser.add_argument('--mode', choices=['fast', 'balanced', 'deep', 'creative', 'precise'],
                           default='balanced', help='Initial processing mode')
    cli_parser.add_argument('--reasoning', choices=['analytical', 'creative', 'logical', 'emotional', 'strategic', 'ethical'],
                           default='analytical', help='Initial reasoning type')
    cli_parser.add_argument('--monitor', action='store_true', 
                           help='Enable real-time monitoring by default')
    
    # Web interface options  
    web_parser = subparsers.add_parser('web', help='Start advanced web interface')
    web_parser.add_argument('--config', default='config/advanced_config.json',
                           help='Configuration file path')
    web_parser.add_argument('--host', default='127.0.0.1', 
                           help='Host to bind web server to')
    web_parser.add_argument('--port', type=int, default=8000,
                           help='Port to bind web server to')
    
    # Global options
    parser.add_argument('--version', action='version', version='MarkAI Advanced 1.0.0')
    parser.add_argument('--banner', action='store_true', 
                       help='Show banner and capabilities')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       default='INFO', help='Set logging level')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug mode')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Show banner if requested or no interface specified
    if args.banner or not args.interface:
        show_banner()
        if args.banner:
            return 0
        if not args.interface:
            print("\nPlease specify an interface: 'cli' or 'web'")
            parser.print_help()
            return 0
    
    # Setup directories and logging
    setup_directories()
    
    # Setup logging
    log_level = 'DEBUG' if args.debug else args.log_level
    setup_logging(
        log_level=log_level,
        log_file='logs/markai.log',
        max_size='50MB',
        backup_count=5
    )
    
    logger = get_logger(__name__)
    logger.info(f"Starting MarkAI Advanced v1.0.0 in {args.interface} mode")
    
    # Start requested interface
    try:
        if args.interface == 'cli':
            return asyncio.run(start_cli_interface(
                args.config,
                processing_mode=args.mode,
                reasoning_type=args.reasoning,
                monitor=args.monitor
            ))
        elif args.interface == 'web':
            return asyncio.run(start_web_interface(
                args.config,
                host=args.host,
                port=args.port
            ))
    except KeyboardInterrupt:
        logger.info("Shutting down MarkAI...")
        print("\n👋 Goodbye!")
        return 0
    except FileNotFoundError as e:
        print(f"Configuration file not found: {e}")
        print("Please run: python scripts/setup.py --configure")
        return 1
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please run: python scripts/setup.py --install")
        return 1
    except Exception as e:
        logger = get_logger(__name__)
        logger.error(f"Startup error: {e}")
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main() or 0)
