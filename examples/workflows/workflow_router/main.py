#!/usr/bin/env python3
"""
간단한 대화형 에이전트 라우터 - 메인 프로그램
Simple Interactive Agent Router - Main Program

이 프로그램은 사용자 요청을 적절한 에이전트로 라우팅합니다.
This program routes user requests to appropriate agents.
"""

import asyncio
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가 / Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from src.routing.simple_router import SimpleRouter
from src.utils.simple_config import SimpleConfig


console = Console()


async def main():
    """메인 프로그램 실행 / Run main program"""
    
    # 환영 메시지 출력 / Display welcome message
    console.print(Panel.fit(
        "[bold green]🚀 Interactive Modular Agent Router[/bold green]\n"
        "간단하고 똑똑한 에이전트 라우터입니다!\n"
        "Simple and smart agent router!",
        title="Welcome",
        border_style="green"
    ))
    
    # 설정 확인 / Check configuration
    config = SimpleConfig()
    if not config.has_required_keys():
        console.print(Panel(
            "[red]⚠️  Anthropic API 키가 필요합니다![/red]\n"
            "[red]⚠️  Anthropic API key required![/red]\n\n"
            "mcp_agent.secrets.yaml 파일을 설정해주세요.\n"
            "Please configure mcp_agent.secrets.yaml file.",
            title="Configuration Required",
            border_style="red"
        ))
        return
    
    # 라우터 초기화 / Initialize router
    console.print("🔧 라우터 초기화 중... / Initializing router...")
    router = SimpleRouter()
    
    # 메인 루프 / Main loop
    while True:
        try:
            # 메뉴 표시 / Show menu
            console.print(Panel.fit(
                "[bold blue]메뉴 / Menu[/bold blue]\n\n"
                "[green]1.[/green] 요청 처리 / Process Request\n"
                "[green]2.[/green] 에이전트 목록 / List Agents\n"
                "[green]3.[/green] 요청 분석 / Analyze Request\n"
                "[green]4.[/green] 종료 / Exit",
                title="Main Menu",
                border_style="blue"
            ))
            
            choice = Prompt.ask("선택 / Choice", choices=["1", "2", "3", "4"], default="1")
            
            if choice == "1":
                await process_request(router)
            elif choice == "2":
                list_agents(router)
            elif choice == "3":
                analyze_request(router)
            elif choice == "4":
                console.print("[bold blue]👋 안녕히 가세요! / Goodbye![/bold blue]")
                break
            
            if choice != "4":
                if not Confirm.ask("계속하시겠습니까? / Continue?", default=True):
                    console.print("[bold blue]👋 안녕히 가세요! / Goodbye![/bold blue]")
                    break
                    
        except KeyboardInterrupt:
            console.print("\n[yellow]⚠️  사용자가 중단했습니다. / Interrupted by user.[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]❌ 오류 / Error: {str(e)}[/red]")


async def process_request(router):
    """요청 처리 / Process request"""
    console.print("\n[bold green]요청을 입력하세요 / Enter your request:[/bold green]")
    console.print("[dim]예시 / Examples: 'search for docs', 'send slack message', 'scrape website'[/dim]")
    
    request = Prompt.ask("요청 / Request")
    if not request.strip():
        console.print("[red]유효한 요청을 입력해주세요. / Please enter a valid request.[/red]")
        return
    
    console.print(f"\n[bold]처리 중 / Processing: '{request}'[/bold]")
    
    # 라우팅 수행 / Perform routing
    agent_name, method = await router.route(request)
    
    if agent_name:
        agent = router.get_agent(agent_name)
        console.print(f"[bold green]✅ 라우팅 완료 / Routed to:[/bold green] {agent_name}")
        console.print(f"[bold]방법 / Method:[/bold] {method}")
        console.print(f"[bold]에이전트 / Agent:[/bold] {agent.name}")
        
        if Confirm.ask("이 에이전트로 실행하시겠습니까? / Execute with this agent?"):
            console.print("[bold yellow]실행 중 / Executing...[/bold yellow]")
            console.print("[bold green]✅ 실행 완료 (시뮬레이션) / Execution complete (simulated)[/bold green]")
    else:
        console.print("[red]❌ 적절한 에이전트를 찾을 수 없습니다. / No suitable agent found.[/red]")


def list_agents(router):
    """에이전트 목록 표시 / List agents"""
    agents = router.list_agents()
    console.print(f"\n[bold blue]사용 가능한 에이전트 / Available Agents ({len(agents)}):[/bold blue]")
    
    for i, agent_name in enumerate(agents, 1):
        agent = router.get_agent(agent_name)
        console.print(f"[green]{i}.[/green] [bold]{agent_name}[/bold] - {agent.name}")


def analyze_request(router):
    """요청 분석 / Analyze request"""
    console.print("\n[bold green]분석할 요청을 입력하세요 / Enter request to analyze:[/bold green]")
    
    request = Prompt.ask("요청 / Request")
    if not request.strip():
        console.print("[red]유효한 요청을 입력해주세요. / Please enter a valid request.[/red]")
        return
    
    analysis = router.analyze(request)
    
    console.print(f"\n[bold blue]분석 결과 / Analysis Results:[/bold blue]")
    console.print(f"[bold]요청 / Request:[/bold] {analysis['request']}")
    console.print(f"[bold]추천 / Recommended:[/bold] {analysis['recommended'] or 'None'}")
    console.print(f"[bold]방법 / Method:[/bold] {analysis['method']}")
    
    console.print(f"\n[bold]점수 / Scores:[/bold]")
    for agent_name, data in analysis['scores'].items():
        score = data['score']
        matched = ', '.join(data['matched_keywords']) or 'None'
        console.print(f"  {agent_name}: {score} (matched: {matched})")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n프로그램이 중단되었습니다. / Program interrupted.")
    except Exception as e:
        print(f"치명적 오류 / Fatal error: {str(e)}")
        sys.exit(1)