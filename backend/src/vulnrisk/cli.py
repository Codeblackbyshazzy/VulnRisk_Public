import click
from .core.risk_calculator import EnhancedContextualFramework, VulnerabilityData
import logging

logging.basicConfig(level=logging.INFO)

@click.group()
def cli() -> None:
    """VulnRisk - Contextual Vulnerability Risk Scoring"""
    pass

@cli.command()
@click.option('--cve', required=True, help='CVE identifier')
@click.option('--cvss', required=True, type=float, help='CVSS score (0-10)')
@click.option('--criticality', required=True, type=int, help='Asset criticality (1-10)')
@click.option('--epss', required=True, type=float, help='EPSS score (0-1)')
@click.option('--internet-facing', is_flag=True, help='Asset is internet-facing')
@click.option('--framework', default='enhanced', help='Risk framework to use')
def score(cve: str, cvss: float, criticality: int, epss: float, internet_facing: bool, framework: str) -> None:
    """Calculate risk score for a single vulnerability"""
    try:
        if not (0 <= cvss <= 10):
            raise ValueError("CVSS score must be between 0 and 10.")
        if not (1 <= criticality <= 10):
            raise ValueError("Asset criticality must be between 1 and 10.")
        if not (0 <= epss <= 1):
            raise ValueError("EPSS score must be between 0 and 1.")

        vuln = VulnerabilityData(
            cve_id=cve,
            cvss_score=cvss,
            asset_criticality=criticality,
            epss_score=epss,
            is_internet_facing=internet_facing
        )

        if framework == 'enhanced':
            calculator = EnhancedContextualFramework()
        else:
            click.echo(f"Framework '{framework}' not supported yet")
            return

        result = calculator.calculate_risk(vuln)

        click.echo(f"\n🎯 Risk Assessment for {cve}")
        click.echo(f"Score: {result.score:.2f}")
        click.echo(f"Priority: {result.priority}")
        click.echo(f"Remediation Timeline: {result.timeline_days} days")
        click.echo(f"\nExplanation:\n{result.explanation}")
    except Exception as e:
        logging.error(f"Error calculating risk: {e}")
        click.echo("An error occurred. Please check your input values.")

if __name__ == '__main__':
    cli() 