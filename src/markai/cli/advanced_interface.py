"""
Advanced CLI Interface - Enterprise-grade command line experience

Features:
- Multi-modal conversations (text, images, files)
- Advanced reasoning mode selection
- Real-time cognitive state monitoring
- Conversation branching and management
- Advanced export and analysis features
- Interactive data visualization
- Plugin ecosystem management
"""

import asyncio
import sys
import json
from typing import Optional, Dict, Any, List
from datetime import datetime
from pathlib import Path
import argparse
import shutil
from dataclasses import asdict

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.table import Table
from rich.live import Live
from rich.spinner import Spinner
from rich.markdown import Markdown
from rich.tree import Tree
from rich.progress import Progress, TaskID, BarColumn, TextColumn, TimeRemainingColumn
from rich.layout import Layout
from rich.columns import Columns
from rich.align import Align

# Setup imports
# from utils.import_helper import setup_project_imports
# setup_project_imports()

from ..core.advanced_ai_engine import AdvancedMarkAICore, ProcessingMode, ReasoningType
from ..utils.config import Config
from ..utils.logger import get_logger


class AdvancedCLIInterface:
    """
    Advanced Command Line Interface with enterprise features
    """
    
    def __init__(self, ai_engine: AdvancedMarkAICore, config: Config):
        self.ai_engine = ai_engine
        self.config = config
        self.console = Console()
        self.logger = get_logger(__name__)
        
        # CLI State
        self.user_id = "cli_user"
        self.conversation_id = None
        self.current_mode = ProcessingMode.BALANCED
        self.current_reasoning = ReasoningType.ANALYTICAL
        
        # Command history
        self.command_history = []
        self.conversation_branches = {}
        
        # Advanced features
        self.monitoring_enabled = False
        self.auto_save = True
        self.export_format = "markdown"
        
        # Setup commands
        self.commands = {
            "help": self._show_help,
            "mode": self._change_processing_mode,
            "reasoning": self._change_reasoning_type,
            "status": self._show_cognitive_status,
            "monitor": self._toggle_monitoring,
            "branch": self._manage_conversation_branches,
            "export": self._advanced_export,
            "analyze": self._analyze_conversation,
            "plugins": self._manage_plugins,
            "settings": self._manage_settings,
            "history": self._show_advanced_history,
            "clear": self._clear_screen,
            "new": self._new_conversation,
            "load": self._load_conversation,
            "save": self._save_conversation,
            "stats": self._show_detailed_stats,
            "debug": self._debug_mode,
            "quit": self._quit
        }
    
    async def start(self):
        """Start the advanced CLI interface"""
        self.console.clear()
        await self._show_advanced_welcome()
        
        # Initialize conversation
        self.conversation_id = await self.ai_engine.conversation_manager.create_conversation(self.user_id)
        
        try:
            while True:
                try:
                    # Show status bar if monitoring enabled
                    if self.monitoring_enabled:
                        await self._show_status_bar()
                    
                    # Get user input with advanced prompt
                    user_input = self._get_advanced_input()
                    
                    if not user_input.strip():
                        continue
                    
                    # Add to history
                    self.command_history.append({
                        'timestamp': datetime.now(),
                        'input': user_input,
                        'mode': self.current_mode.value,
                        'reasoning': self.current_reasoning.value
                    })
                    
                    # Check for commands
                    if user_input.startswith("/"):
                        await self._handle_advanced_command(user_input[1:])
                        continue
                    
                    # Process as advanced message
                    await self._process_advanced_message(user_input)
                    
                except KeyboardInterrupt:
                    if await self._handle_interrupt():
                        break
                except Exception as e:
                    self.console.print(f"[red]Error: {str(e)}[/red]")
                    self.logger.error(f"CLI error: {e}")
        
        finally:
            await self._shutdown_gracefully()
    
    def _get_advanced_input(self) -> str:
        """Get user input with advanced prompt showing current state"""
        # Create status indicators
        mode_color = {
            ProcessingMode.FAST: "yellow",
            ProcessingMode.BALANCED: "blue", 
            ProcessingMode.DEEP: "purple",
            ProcessingMode.CREATIVE: "magenta",
            ProcessingMode.PRECISE: "green"
        }.get(self.current_mode, "white")
        
        reasoning_color = {
            ReasoningType.ANALYTICAL: "cyan",
            ReasoningType.CREATIVE: "magenta",
            ReasoningType.LOGICAL: "green",
            ReasoningType.EMOTIONAL: "red",
            ReasoningType.STRATEGIC: "yellow",
            ReasoningType.ETHICAL: "blue"
        }.get(self.current_reasoning, "white")
        
        # Create prompt with status
        prompt_text = f"[bold blue]You[/bold blue] " \
                     f"[dim][[{mode_color}]{self.current_mode.value}[/{mode_color}]|" \
                     f"[{reasoning_color}]{self.current_reasoning.value}[/{reasoning_color}]][/dim]"
        
        return Prompt.ask(prompt_text, console=self.console)
    
    async def _show_advanced_welcome(self):
        """Show advanced welcome screen with capabilities"""
        welcome_panel = Panel.fit(
            """[bold cyan]MarkAI Advanced CLI Interface[/bold cyan]
            
🧠 [bold]Cognitive Capabilities:[/bold]
   • Multi-modal reasoning (analytical, creative, strategic, ethical)
   • Advanced memory networks with episodic & semantic memory
   • Chain-of-thought reasoning with meta-cognition
   • Real-time cognitive state monitoring
   • Adaptive learning and personalization

🔧 [bold]Advanced Features:[/bold]
   • Conversation branching and management
   • Multi-modal input (text, images, documents)
   • Advanced export and analysis tools
   • Plugin ecosystem with AI-powered tools
   • Real-time performance monitoring

📋 [bold]Quick Commands:[/bold]
   /help - Show all commands    /mode - Change processing mode
   /reasoning - Set reasoning    /status - Show cognitive state
   /monitor - Toggle monitoring  /plugins - Manage plugins

[dim]Type /help for full command list or start chatting![/dim]""",
            title="🚀 Advanced AI Assistant",
            border_style="bright_blue"
        )
        
        self.console.print(welcome_panel)
        self.console.print()
    
    async def _process_advanced_message(self, message: str):
        """Process message with advanced AI capabilities"""
        with self.console.status("🧠 Advanced AI processing...", spinner="dots"):
            try:
                # Process with advanced engine
                response = await self.ai_engine.process_advanced_message(
                    message=message,
                    user_id=self.user_id,
                    conversation_id=self.conversation_id,
                    processing_mode=self.current_mode,
                    reasoning_type=self.current_reasoning
                )
                
                # Update conversation ID
                if 'conversation_id' in response.metadata:
                    self.conversation_id = response.metadata['conversation_id']
                
            except Exception as e:
                self.logger.error(f"Advanced processing error: {e}")
                self.console.print(f"[red]Processing error: {str(e)}[/red]")
                return
        
        # Display advanced response
        await self._display_advanced_response(response)
    
    async def _display_advanced_response(self, response):
        """Display advanced AI response with full details"""
        # Main response content
        try:
            markdown_content = Markdown(response.content)
            self.console.print(Panel(
                markdown_content,
                title="🤖 MarkAI Advanced Response",
                border_style="green",
                padding=(1, 2)
            ))
        except Exception:
            self.console.print(Panel(
                response.content,
                title="🤖 MarkAI Response", 
                border_style="green",
                padding=(1, 2)
            ))
        
        # Show advanced metadata if detailed mode
        if self.monitoring_enabled:
            await self._show_response_details(response)
    
    async def _show_response_details(self, response):
        """Show detailed response analysis"""
        # Create details table
        details_table = Table(title="🔍 Response Analysis", border_style="cyan")
        details_table.add_column("Metric", style="cyan", width=20)
        details_table.add_column("Value", style="white", width=30)
        details_table.add_column("Details", style="dim", width=40)
        
        details_table.add_row(
            "Confidence", 
            f"{response.confidence:.2%}",
            "AI confidence in response accuracy"
        )
        details_table.add_row(
            "Processing Time",
            f"{response.metadata.get('processing_time', 0):.2f}s", 
            "Total processing duration"
        )
        details_table.add_row(
            "Reasoning Steps",
            str(len(response.reasoning_steps)),
            "Chain-of-thought reasoning depth"
        )
        details_table.add_row(
            "Tokens Used",
            str(response.tokens_used),
            "Computational resources consumed"
        )
        details_table.add_row(
            "Safety Score",
            f"{response.safety_assessment.get('safety_score', 0.95):.2%}",
            "Content safety and alignment"
        )
        
        self.console.print(details_table)
        
        # Show reasoning steps if available
        if response.reasoning_steps and len(response.reasoning_steps) > 0:
            reasoning_tree = Tree("🧠 Reasoning Process")
            for step in response.reasoning_steps[:5]:  # Show first 5 steps
                reasoning_tree.add(f"[dim]{step.thought[:60]}...[/dim]")
            self.console.print(reasoning_tree)
    
    async def _handle_advanced_command(self, command: str):
        """Handle advanced CLI commands"""
        parts = command.strip().split()
        if not parts:
            return
        
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        if cmd in self.commands:
            try:
                await self.commands[cmd](args)
            except Exception as e:
                self.console.print(f"[red]Command error: {str(e)}[/red]")
        else:
            self.console.print(f"[red]Unknown command: {cmd}. Type /help for available commands.[/red]")
    
    async def _show_help(self, args: List[str]):
        """Show comprehensive help information"""
        help_layout = Layout()
        help_layout.split_column(
            Layout(name="commands", ratio=2),
            Layout(name="features", ratio=1)
        )
        
        # Commands table
        commands_table = Table(title="📋 Advanced Commands", border_style="blue")
        commands_table.add_column("Command", style="cyan", width=15)
        commands_table.add_column("Description", style="white", width=50)
        commands_table.add_column("Examples", style="dim", width=30)
        
        command_info = {
            "/help": ("Show this help", "/help, /help plugins"),
            "/mode": ("Change processing mode", "/mode deep, /mode creative"),
            "/reasoning": ("Set reasoning type", "/reasoning creative, /reasoning ethical"), 
            "/status": ("Show cognitive state", "/status"),
            "/monitor": ("Toggle monitoring", "/monitor on, /monitor off"),
            "/branch": ("Manage conversations", "/branch new, /branch list"),
            "/export": ("Export conversations", "/export md, /export json"),
            "/analyze": ("Analyze conversation", "/analyze patterns, /analyze sentiment"),
            "/plugins": ("Manage plugins", "/plugins list, /plugins enable research"),
            "/settings": ("Manage settings", "/settings view, /settings set auto_save true"),
            "/quit": ("Exit application", "/quit")
        }
        
        for cmd, (desc, examples) in command_info.items():
            commands_table.add_row(cmd, desc, examples)
        
        help_layout["commands"].update(Panel(commands_table, border_style="blue"))
        
        # Features panel
        features_text = """[bold]🚀 Advanced Features:[/bold]

[cyan]Processing Modes:[/cyan]
• fast - Quick responses
• balanced - Speed/quality balance  
• deep - Thorough analysis
• creative - Maximum creativity
• precise - Highest accuracy

[cyan]Reasoning Types:[/cyan]
• analytical - Systematic analysis
• creative - Innovative thinking
• logical - Structured reasoning
• emotional - Empathetic responses
• strategic - Long-term planning
• ethical - Moral considerations

[cyan]Monitoring:[/cyan]
• Real-time cognitive state
• Response quality metrics
• Processing performance
• Safety assessments"""
        
        help_layout["features"].update(Panel(features_text, title="Features", border_style="green"))
        
        self.console.print(help_layout)
    
    async def _change_processing_mode(self, args: List[str]):
        """Change AI processing mode"""
        if not args:
            # Show current mode and options
            modes_table = Table(title="🔧 Processing Modes", border_style="yellow")
            modes_table.add_column("Mode", style="cyan")
            modes_table.add_column("Description", style="white") 
            modes_table.add_column("Best For", style="dim")
            modes_table.add_column("Current", style="green")
            
            mode_info = {
                "fast": ("Quick responses with minimal processing", "Simple questions, quick tasks"),
                "balanced": ("Balance between speed and quality", "General conversations"),
                "deep": ("Thorough analysis and reasoning", "Complex problems, research"),
                "creative": ("Maximum creativity and innovation", "Brainstorming, creative tasks"),
                "precise": ("Highest accuracy and fact-checking", "Critical information, analysis")
            }
            
            for mode_name, (desc, best_for) in mode_info.items():
                current = "✓" if mode_name == self.current_mode.value else ""
                modes_table.add_row(mode_name, desc, best_for, current)
            
            self.console.print(modes_table)
            return
        
        mode_name = args[0].lower()
        try:
            new_mode = ProcessingMode(mode_name)
            self.current_mode = new_mode
            self.console.print(f"[green]✓ Processing mode changed to: {mode_name}[/green]")
        except ValueError:
            self.console.print(f"[red]Invalid mode: {mode_name}. Use: fast, balanced, deep, creative, precise[/red]")
    
    async def _change_reasoning_type(self, args: List[str]):
        """Change AI reasoning type"""
        if not args:
            # Show current reasoning and options
            reasoning_table = Table(title="🧠 Reasoning Types", border_style="purple")
            reasoning_table.add_column("Type", style="cyan")
            reasoning_table.add_column("Description", style="white")
            reasoning_table.add_column("Current", style="green")
            
            reasoning_info = {
                "analytical": "Systematic analysis and data-driven reasoning",
                "creative": "Innovative and out-of-the-box thinking",
                "logical": "Structured, step-by-step logical reasoning", 
                "emotional": "Empathetic and emotionally-aware responses",
                "strategic": "Long-term planning and strategic thinking",
                "ethical": "Moral and ethical considerations in reasoning"
            }
            
            for reasoning_name, desc in reasoning_info.items():
                current = "✓" if reasoning_name == self.current_reasoning.value else ""
                reasoning_table.add_row(reasoning_name, desc, current)
            
            self.console.print(reasoning_table)
            return
        
        reasoning_name = args[0].lower()
        try:
            new_reasoning = ReasoningType(reasoning_name)
            self.current_reasoning = new_reasoning
            self.console.print(f"[green]✓ Reasoning type changed to: {reasoning_name}[/green]")
        except ValueError:
            valid_types = ", ".join([rt.value for rt in ReasoningType])
            self.console.print(f"[red]Invalid reasoning type: {reasoning_name}. Use: {valid_types}[/red]")
    
    async def _show_cognitive_status(self, args: List[str]):
        """Show current cognitive status"""
        status = await self.ai_engine.get_cognitive_status()
        
        # Create status layout
        status_layout = Layout()
        status_layout.split_row(
            Layout(name="current_state", ratio=1),
            Layout(name="capabilities", ratio=1)
        )
        
        # Current state
        state_table = Table(title="🧠 Current Cognitive State", border_style="cyan")
        state_table.add_column("Aspect", style="cyan")
        state_table.add_column("Value", style="white")
        
        cognitive_state = status['cognitive_state']
        state_table.add_row("Reasoning Mode", cognitive_state['reasoning_mode'])
        state_table.add_row("Processing Mode", cognitive_state['processing_mode'])
        state_table.add_row("Confidence Level", f"{cognitive_state['confidence_level']:.2%}")
        state_table.add_row("Learning Rate", f"{cognitive_state['learning_rate']:.2%}")
        state_table.add_row("Curiosity Level", f"{cognitive_state['curiosity_level']:.2%}")
        
        status_layout["current_state"].update(Panel(state_table, border_style="cyan"))
        
        # Capabilities
        capabilities_text = f"""[bold]🚀 Advanced Capabilities:[/bold]

[cyan]Memory Statistics:[/cyan]
• Episodic memories: {status['memory_stats']['episodic_memories']}
• Semantic memories: {status['memory_stats']['semantic_memories']}

[cyan]Reasoning Modes:[/cyan]
{', '.join(status['reasoning_capabilities'])}

[cyan]Processing Modes:[/cyan]
{', '.join(status['processing_modes'])}

[cyan]Multimodal Support:[/cyan]
{', '.join(status['multimodal_support'])}

[cyan]Advanced Features:[/cyan]
"""
        for feature in status['advanced_features']:
            capabilities_text += f"• {feature.replace('_', ' ').title()}\n"
        
        status_layout["capabilities"].update(Panel(capabilities_text, title="Capabilities", border_style="green"))
        
        self.console.print(status_layout)
    
    async def _toggle_monitoring(self, args: List[str]):
        """Toggle real-time monitoring"""
        if args and args[0].lower() in ['on', 'true', 'enable']:
            self.monitoring_enabled = True
            action = "enabled"
        elif args and args[0].lower() in ['off', 'false', 'disable']:
            self.monitoring_enabled = False
            action = "disabled"
        else:
            self.monitoring_enabled = not self.monitoring_enabled
            action = "enabled" if self.monitoring_enabled else "disabled"
        
        self.console.print(f"[green]✓ Real-time monitoring {action}[/green]")
    
    async def _show_status_bar(self):
        """Show real-time status bar"""
        status_text = f"Mode: {self.current_mode.value} | Reasoning: {self.current_reasoning.value} | Monitoring: ON"
        self.console.print(f"[dim]{status_text}[/dim]")
    
    async def _advanced_export(self, args: List[str]):
        """Advanced conversation export"""
        if not self.conversation_id:
            self.console.print("[yellow]No active conversation to export.[/yellow]")
            return
        
        export_format = args[0] if args else self.export_format
        
        try:
            # Get conversation history
            history = await self.ai_engine.conversation_manager.get_history(self.conversation_id)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if export_format.lower() in ['md', 'markdown']:
                filename = f"conversation_{timestamp}.md"
                await self._export_markdown(history, filename)
            elif export_format.lower() == 'json':
                filename = f"conversation_{timestamp}.json"
                await self._export_json(history, filename)
            elif export_format.lower() == 'html':
                filename = f"conversation_{timestamp}.html"
                await self._export_html(history, filename)
            else:
                self.console.print(f"[red]Unsupported format: {export_format}. Use: md, json, html[/red]")
                return
            
            self.console.print(f"[green]✓ Conversation exported to: {filename}[/green]")
            
        except Exception as e:
            self.console.print(f"[red]Export error: {str(e)}[/red]")
    
    async def _export_markdown(self, history: List[Dict], filename: str):
        """Export conversation as markdown"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# MarkAI Advanced Conversation Export\n\n")
            f.write(f"**Export Date:** {datetime.now().isoformat()}\n")
            f.write(f"**Conversation ID:** {self.conversation_id}\n")
            f.write(f"**Total Exchanges:** {len(history)}\n\n")
            f.write("---\n\n")
            
            for i, exchange in enumerate(history, 1):
                f.write(f"## Exchange {i}\n\n")
                f.write(f"**Timestamp:** {exchange.get('timestamp', 'Unknown')}\n\n")
                f.write(f"**You:**\n{exchange.get('user_message', '')}\n\n")
                f.write(f"**MarkAI:**\n{exchange.get('ai_response', '')}\n\n")
                f.write("---\n\n")
    
    async def _quit(self, args: List[str]):
        """Quit the application"""
        if self.auto_save and self.conversation_id:
            with self.console.status("Saving conversation..."):
                # Auto-save current conversation
                await self._save_conversation(['auto_save'])
        
        self.console.print("[green]Thank you for using MarkAI Advanced CLI! 👋[/green]")
        sys.exit(0)
    
    async def _shutdown_gracefully(self):
        """Graceful shutdown"""
        self.console.print("\n[yellow]Shutting down MarkAI...[/yellow]")
        await self.ai_engine.shutdown()
        self.console.print("[green]Goodbye! 👋[/green]")


async def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="MarkAI Advanced CLI Interface")
    parser.add_argument("--config", default="config/config.json", help="Configuration file")
    parser.add_argument("--mode", choices=['fast', 'balanced', 'deep', 'creative', 'precise'], 
                       default='balanced', help="Initial processing mode")
    parser.add_argument("--reasoning", choices=['analytical', 'creative', 'logical', 'emotional', 'strategic', 'ethical'],
                       default='analytical', help="Initial reasoning type")
    parser.add_argument("--monitor", action='store_true', help="Enable monitoring by default")
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        config = Config(args.config)
        
        # Initialize advanced AI engine
        ai_engine = AdvancedMarkAICore(config)
        
        # Create and start CLI interface
        cli = AdvancedCLIInterface(ai_engine, config)
        
        # Set initial modes
        cli.current_mode = ProcessingMode(args.mode)
        cli.current_reasoning = ReasoningType(args.reasoning)
        cli.monitoring_enabled = args.monitor
        
        await cli.start()
        
    except KeyboardInterrupt:
        print("\nGoodbye! 👋")
    except Exception as e:
        print(f"Error starting MarkAI Advanced CLI: {e}")


if __name__ == "__main__":
    asyncio.run(main())
