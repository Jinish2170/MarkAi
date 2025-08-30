"""
Command Line Interface for MarkAI
"""

import asyncio
import sys
from typing import Optional, Dict, Any
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.live import Live
from rich.spinner import Spinner
from rich.markdown import Markdown

from ..core.ai_engine import MarkAICore
from ..utils.config import Config
from ..utils.logger import get_logger


class CLIInterface:
    """Command-line interface for MarkAI"""
    
    def __init__(self, ai_engine: MarkAICore, config: Config):
        self.ai_engine = ai_engine
        self.config = config
        self.console = Console()
        self.logger = get_logger(__name__)
        
        # Current session data
        self.user_id = "cli_user"
        self.conversation_id: Optional[str] = None
        self.session_start = datetime.now()
        
        # CLI commands
        self.commands = {
            "help": self._show_help,
            "clear": self._clear_screen,
            "history": self._show_history,
            "stats": self._show_stats,
            "preferences": self._manage_preferences,
            "plugins": self._show_plugins,
            "context": self._show_context,
            "export": self._export_conversation,
            "new": self._new_conversation,
            "quit": self._quit,
            "exit": self._quit,
        }
    
    async def start(self):
        """Start the CLI interface"""
        self._show_welcome()
        
        try:
            while True:
                try:
                    # Get user input
                    user_input = Prompt.ask(
                        "\n[bold blue]You[/bold blue]",
                        console=self.console
                    ).strip()
                    
                    if not user_input:
                        continue
                    
                    # Check for commands
                    if user_input.startswith("/"):
                        await self._handle_command(user_input[1:])
                        continue
                    
                    # Process as regular message
                    await self._process_message(user_input)
                    
                except KeyboardInterrupt:
                    if Confirm.ask("\n[yellow]Do you want to quit?[/yellow]"):
                        break
                    else:
                        continue
                        
        except (EOFError, KeyboardInterrupt):
            self.console.print(f"[yellow]Interrupted by user[/yellow]")
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")
        
        self._show_goodbye()
    
    def _show_welcome(self):
        """Display welcome message"""
        welcome_text = Text()
        welcome_text.append("🤖 MarkAI - Advanced AI Assistant\n", style="bold magenta")
        welcome_text.append("Powered by Google Gemini\n\n", style="dim")
        welcome_text.append("Commands:\n", style="bold")
        welcome_text.append("  /help     - Show help\n", style="cyan")
        welcome_text.append("  /history  - Show conversation history\n", style="cyan")
        welcome_text.append("  /stats    - Show statistics\n", style="cyan")
        welcome_text.append("  /plugins  - Show available plugins\n", style="cyan")
        welcome_text.append("  /quit     - Exit MarkAI\n\n", style="cyan")
        welcome_text.append("Type your message or use /help for more commands.", style="dim")
        
        self.console.print(Panel(welcome_text, title="Welcome", border_style="blue"))
    
    def _show_goodbye(self):
        """Display goodbye message"""
        session_duration = datetime.now() - self.session_start
        goodbye_text = f"Thanks for using MarkAI!\nSession duration: {session_duration}"
        
        self.console.print(Panel(
            goodbye_text,
            title="Goodbye",
            border_style="green"
        ))
    
    async def _process_message(self, message: str):
        """Process a user message"""
        # Show thinking indicator
        with Live(
            Spinner("dots", text="MarkAI is thinking..."),
            console=self.console,
            refresh_per_second=10
        ):
            try:
                # Process through AI engine
                response = await self.ai_engine.process_message(
                    message=message,
                    user_id=self.user_id,
                    conversation_id=self.conversation_id
                )
                
                # Update conversation ID
                self.conversation_id = response.metadata.get('conversation_id')
                
            except (ConnectionError, TimeoutError) as e:
                self.logger.error(f"Network error processing message: {str(e)}")
                self.console.print(f"[red]Network error: {str(e)}[/red]")
                return
            except Exception as e:
                self.logger.error(f"Error processing message: {str(e)}")
                self.console.print(f"[red]Error: {str(e)}[/red]")
                return
        
        # Display AI response
        self._display_ai_response(response)
    
    def _display_ai_response(self, response):
        """Display AI response with formatting"""
        # Create response panel
        response_text = Text()
        response_text.append("🤖 ", style="bold blue")
        response_text.append("MarkAI\n\n", style="bold blue")
        
        # Try to render as markdown if it contains markdown syntax
        content = response.content
        if any(marker in content for marker in ['**', '*', '`', '#', '-', '1.']):
            try:
                markdown_content = Markdown(content)
                self.console.print(Panel(
                    markdown_content,
                    title="MarkAI Response",
                    border_style="green"
                ))
            except (ValueError, TypeError) as e:
                # Fallback to plain text for markdown parsing errors
                response_text.append(content, style="white")
                self.console.print(Panel(
                    response_text,
                    title="MarkAI Response",
                    border_style="green"
                ))
        else:
            response_text.append(content, style="white")
            self.console.print(Panel(
                response_text,
                title="MarkAI Response",
                border_style="green"
            ))
        
        # Show metadata if available
        if response.reasoning_steps:
            self._show_reasoning_steps(response.reasoning_steps)
        
        # Show quick stats
        stats_text = f"Confidence: {response.confidence:.1%} | Tokens: {response.tokens_used} | Model: {response.model_used}"
        self.console.print(f"[dim]{stats_text}[/dim]")
    
    def _show_reasoning_steps(self, steps):
        """Display reasoning steps"""
        if not steps:
            return
        
        reasoning_table = Table(title="Reasoning Steps", show_header=False, border_style="yellow")
        reasoning_table.add_column("Step", style="cyan", width=60)
        
        for i, step in enumerate(steps, 1):
            reasoning_table.add_row(f"{i}. {step}")
        
        self.console.print(reasoning_table)
    
    async def _handle_command(self, command: str):
        """Handle CLI commands"""
        parts = command.strip().split()
        if not parts:
            return
        
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        if cmd in self.commands:
            try:
                await self.commands[cmd](args)
            except (ValueError, TypeError) as e:
                self.console.print(f"[red]Invalid command arguments: {str(e)}[/red]")
            except Exception as e:
                self.console.print(f"[red]Command error: {str(e)}[/red]")
        else:
            self.console.print(f"[red]Unknown command: {cmd}. Type /help for available commands.[/red]")
    
    async def _show_help(self, args):
        """Show help information"""
        help_table = Table(title="MarkAI CLI Commands", border_style="blue")
        help_table.add_column("Command", style="cyan", width=15)
        help_table.add_column("Description", style="white")
        
        commands_info = {
            "/help": "Show this help message",
            "/clear": "Clear the screen",
            "/history": "Show conversation history",
            "/stats": "Show user statistics",
            "/preferences": "Manage user preferences",
            "/plugins": "Show available plugins",
            "/context": "Show current context",
            "/export": "Export conversation",
            "/new": "Start new conversation",
            "/quit": "Exit MarkAI"
        }
        
        for cmd, desc in commands_info.items():
            help_table.add_row(cmd, desc)
        
        self.console.print(help_table)
    
    async def _clear_screen(self, args):
        """Clear the screen"""
        self.console.clear()
        self._show_welcome()
    
    async def _show_history(self, args):
        """Show conversation history"""
        if not self.conversation_id:
            self.console.print("[yellow]No active conversation.[/yellow]")
            return
        
        try:
            history = await self.ai_engine.conversation_manager.get_history(
                self.conversation_id, limit=10
            )
            
            if not history:
                self.console.print("[yellow]No conversation history found.[/yellow]")
                return
            
            history_table = Table(title="Conversation History", border_style="cyan")
            history_table.add_column("Time", style="dim", width=20)
            history_table.add_column("You", style="blue", width=40)
            history_table.add_column("MarkAI", style="green", width=40)
            
            for entry in history[-5:]:  # Show last 5 entries
                timestamp = entry.get('timestamp', 'Unknown')
                user_msg = entry.get('user_message', '')[:60] + ('...' if len(entry.get('user_message', '')) > 60 else '')
                ai_msg = entry.get('ai_response', '')[:60] + ('...' if len(entry.get('ai_response', '')) > 60 else '')
                
                history_table.add_row(timestamp, user_msg, ai_msg)
            
            self.console.print(history_table)
            
        except (ConnectionError, FileNotFoundError) as e:
            self.console.print(f"[red]Error retrieving history: {str(e)}[/red]")
        except Exception as e:
            self.console.print(f"[red]Unexpected error: {str(e)}[/red]")
    
    async def _show_stats(self, args):
        """Show user statistics"""
        try:
            conv_stats = await self.ai_engine.conversation_manager.get_stats(self.user_id)
            context_stats = await self.ai_engine.context_manager.get_user_stats(self.user_id)
            
            stats_table = Table(title="Your Statistics", border_style="magenta")
            stats_table.add_column("Metric", style="cyan")
            stats_table.add_column("Value", style="white")
            
            stats_table.add_row("Total Conversations", str(conv_stats.get('total_conversations', 0)))
            stats_table.add_row("Total Messages", str(conv_stats.get('total_messages', 0)))
            stats_table.add_row("Total Tokens", str(conv_stats.get('total_tokens', 0)))
            stats_table.add_row("Total Interactions", str(context_stats.get('total_interactions', 0)))
            
            self.console.print(stats_table)
            
        except (ConnectionError, FileNotFoundError) as e:
            self.console.print(f"[red]Error retrieving stats: {str(e)}[/red]")
        except Exception as e:
            self.console.print(f"[red]Error retrieving stats: {str(e)}[/red]")
    
    async def _manage_preferences(self, args):
        """Manage user preferences"""
        try:
            context = await self.ai_engine.context_manager.get_user_context(self.user_id)
            prefs = context.get('preferences', {})
            
            self.console.print("[bold]Current Preferences:[/bold]")
            if prefs:
                for key, value in prefs.items():
                    self.console.print(f"  {key}: {value}")
            else:
                self.console.print("  No preferences set")
            
            # Allow setting preferences
            if Confirm.ask("Would you like to update your preferences?"):
                response_style = Prompt.ask(
                    "Response style",
                    choices=["detailed", "concise", "balanced"],
                    default=prefs.get('response_style', 'balanced')
                )
                
                complexity_level = Prompt.ask(
                    "Complexity level",
                    choices=["beginner", "intermediate", "advanced"],
                    default=prefs.get('complexity_level', 'intermediate')
                )
                
                new_prefs = {
                    'response_style': response_style,
                    'complexity_level': complexity_level
                }
                
                await self.ai_engine.context_manager.update_user_preferences(
                    self.user_id, new_prefs
                )
                
                self.console.print("[green]Preferences updated![/green]")
                
        except (ValueError, KeyError) as e:
            self.console.print(f"[red]Invalid preference: {str(e)}[/red]")
        except Exception as e:
            self.console.print(f"[red]Error managing preferences: {str(e)}[/red]")
    
    async def _show_plugins(self, args):
        """Show available plugins"""
        try:
            plugins = self.ai_engine.plugin_manager.list_plugins()
            
            if not plugins:
                self.console.print("[yellow]No plugins available.[/yellow]")
                return
            
            plugins_table = Table(title="Available Plugins", border_style="yellow")
            plugins_table.add_column("Name", style="cyan", width=20)
            plugins_table.add_column("Version", style="white", width=10)
            plugins_table.add_column("Description", style="white")
            
            for plugin in plugins:
                plugins_table.add_row(
                    plugin.get('name', 'Unknown'),
                    plugin.get('version', '1.0.0'),
                    plugin.get('description', 'No description')
                )
            
            self.console.print(plugins_table)
            
        except (AttributeError, KeyError) as e:
            self.console.print(f"[red]Plugin system error: {str(e)}[/red]")
        except Exception as e:
            self.console.print(f"[red]Error showing plugins: {str(e)}[/red]")
    
    async def _show_context(self, args):
        """Show current user context"""
        try:
            context = await self.ai_engine.context_manager.get_user_context(self.user_id)
            
            context_table = Table(title="Current Context", border_style="cyan")
            context_table.add_column("Attribute", style="cyan")
            context_table.add_column("Value", style="white")
            
            context_table.add_row("User ID", context.get('user_id', 'Unknown'))
            context_table.add_row("Expertise Areas", ', '.join(context.get('expertise_areas', [])))
            context_table.add_row("Communication Style", context.get('communication_style', 'Default'))
            context_table.add_row("Recent Interactions", str(context.get('interaction_count', 0)))
            
            self.console.print(context_table)
            
        except (ConnectionError, FileNotFoundError) as e:
            self.console.print(f"[red]Context data error: {str(e)}[/red]")
        except Exception as e:
            self.console.print(f"[red]Error showing context: {str(e)}[/red]")
    
    async def _export_conversation(self, args):
        """Export current conversation"""
        if not self.conversation_id:
            self.console.print("[yellow]No active conversation to export.[/yellow]")
            return
        
        try:
            history = await self.ai_engine.conversation_manager.get_history(
                self.conversation_id, limit=1000
            )
            
            filename = f"markai_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"MarkAI Conversation Export\n")
                f.write(f"Date: {datetime.now().isoformat()}\n")
                f.write(f"Conversation ID: {self.conversation_id}\n")
                f.write("=" * 50 + "\n\n")
                
                for entry in history:
                    f.write(f"[{entry.get('timestamp', 'Unknown')}]\n")
                    f.write(f"You: {entry.get('user_message', '')}\n")
                    f.write(f"MarkAI: {entry.get('ai_response', '')}\n")
                    f.write("-" * 30 + "\n\n")
            
            self.console.print(f"[green]Conversation exported to {filename}[/green]")
            
        except (IOError, OSError) as e:
            self.console.print(f"[red]File error: {str(e)}[/red]")
        except Exception as e:
            self.console.print(f"[red]Error exporting conversation: {str(e)}[/red]")
    
    async def _new_conversation(self, args):
        """Start a new conversation"""
        if self.conversation_id and Confirm.ask("Start a new conversation? Current conversation will be saved."):
            self.conversation_id = None
            self.console.print("[green]New conversation started![/green]")
        elif not self.conversation_id:
            self.console.print("[yellow]You're already in a new conversation.[/yellow]")
    
    async def _quit(self, args):
        """Quit the CLI"""
        raise KeyboardInterrupt()
