#!/usr/bin/env python3
"""
EliteA Pipeline - Main Entry Point

Automated Confluence documentation generation from GitHub repositories.
"""

import os
import sys
import click
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from elitea.logger import setup_logger
from elitea.config import Config
from elitea.pipeline import EliteAPipeline

logger = setup_logger(__name__)


@click.command()
@click.option(
    "--repo",
    required=True,
    help="GitHub repository URL (e.g., https://github.com/owner/repo)",
)
@click.option(
    "--template",
    default="Technical-App-Manifest-v1",
    help="Template name to use for extraction",
)
@click.option(
    "--space",
    default=None,
    help="Confluence space key (default from config)",
)
@click.option(
    "--parent",
    default=None,
    help="Parent page title in Confluence",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Run without creating/updating Confluence page",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose/debug logging",
)
@click.option(
    "--output",
    default=None,
    help="Save output to file instead of Confluence",
)
@click.option(
    "--update",
    is_flag=True,
    help="Update existing page instead of creating new",
)
@click.version_option(version="1.0.0", prog_name="EliteA")
def main(repo, template, space, parent, dry_run, verbose, output, update):
    """
    EliteA - Automated Confluence Documentation Pipeline

    Extracts technical metadata from GitHub repositories using AI
    and creates structured Confluence documentation.

    Example:
        python main.py --repo https://github.com/company/payment-service --verbose
    """

    try:
        # Configure logging
        if verbose:
            os.environ["LOG_LEVEL"] = "DEBUG"
        
        # Load configuration
        config = Config()
        
        # Validate configuration
        if not config.github_token:
            click.secho("❌ Error: GITHUB_TOKEN not set", fg="red")
            click.echo("Set GITHUB_TOKEN in .env file or environment variable")
            sys.exit(1)
        
        if not config.claude_api_key:
            click.secho("❌ Error: CLAUDE_API_KEY not set", fg="red")
            click.echo("Set CLAUDE_API_KEY in .env file or environment variable")
            sys.exit(1)
        
        if not dry_run and not output:
            if not config.confluence_url or not config.confluence_api_token:
                click.secho("❌ Error: Confluence credentials not set", fg="red")
                click.echo("Set CONFLUENCE_URL and CONFLUENCE_API_TOKEN in .env file")
                click.echo("Or use --dry-run or --output to skip Confluence")
                sys.exit(1)
        
        # Display startup info
        click.secho("=" * 60, fg="cyan")
        click.secho("🚀 EliteA Pipeline v1.0.0", fg="cyan", bold=True)
        click.secho("=" * 60, fg="cyan")
        click.echo()
        
        # Show configuration
        click.echo(f"📦 Repository: {repo}")
        click.echo(f"📋 Template: {template}")
        click.echo(f"📍 Space: {space or config.confluence_space}")
        if parent:
            click.echo(f"👪 Parent Page: {parent}")
        click.echo(f"🔄 Mode: {'DRY RUN (no changes)' if dry_run else 'LIVE (will create/update)'}")
        if output:
            click.echo(f"💾 Output File: {output}")
        click.echo()
        
        # Initialize pipeline
        click.secho("Initializing pipeline...", fg="blue")
        pipeline = EliteAPipeline(
            config=config,
            template_name=template,
            confluence_space=space or config.confluence_space,
            parent_page=parent,
            dry_run=dry_run,
            output_file=output,
            update_existing=update,
        )
        
        # Run pipeline
        click.secho("Starting extraction pipeline...", fg="blue")
        result = pipeline.run(repo)
        
        # Display results
        click.echo()
        click.secho("=" * 60, fg="green")
        click.secho("✅ Pipeline Completed Successfully", fg="green", bold=True)
        click.secho("=" * 60, fg="green")
        click.echo()
        
        # Show summary
        click.echo(f"✓ Fields extracted: {result['fields_extracted']} / {result['total_fields']}")
        click.echo(f"✓ Confidence score: {result['confidence_score']:.1%}")
        
        if not dry_run and not output:
            click.echo(f"✓ Confluence page: {result['page_url']}")
        elif output:
            click.echo(f"✓ Output saved: {output}")
        else:
            click.echo("✓ Dry run completed (no changes made)")
        
        click.echo()
        
        if result.get('warnings'):
            click.secho("⚠️  Warnings:", fg="yellow")
            for warning in result['warnings']:
                click.echo(f"  • {warning}")
        
        if result.get('missing_fields'):
            click.secho("ℹ️  Missing fields (set to [Not Specified]):", fg="yellow")
            for field in result['missing_fields'][:5]:  # Show first 5
                click.echo(f"  • {field}")
            if len(result['missing_fields']) > 5:
                click.echo(f"  ... and {len(result['missing_fields']) - 5} more")
        
        click.echo()
        
    except KeyboardInterrupt:
        click.secho("\n⏸️  Pipeline interrupted by user", fg="yellow")
        sys.exit(130)
    except Exception as e:
        click.secho(f"\n❌ Error: {str(e)}", fg="red")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
