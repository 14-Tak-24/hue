"""
AI Agent Integration Framework
Provides autonomous agent operations with routing rules, quality gates, and project conventions
"""

import json
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
import asyncio
from abc import ABC, abstractmethod

from .souls_manager import SoulsManager
from .openrouter_integration import OpenRouterIntegration
from .content_pipeline import ContentPipeline
from .utils import LoggingUtils


class AgentStatus(Enum):
    """Status of AI agents"""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"
    COMPLETED = "completed"


class AgentPriority(Enum):
    """Priority levels for agent tasks"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class QualityGate(Enum):
    """Quality gate levels"""
    STRICT = "strict"      # High quality requirements, slower processing
    BALANCED = "balanced"  # Balance between quality and speed
    FAST = "fast"         # Prioritize speed over quality
    EXPERIMENTAL = "experimental"  # Testing new approaches


@dataclass
class AgentTask:
    """Task for AI agent execution"""
    task_id: str
    agent_type: str
    priority: AgentPriority
    data: Dict[str, Any]
    quality_gate: QualityGate = QualityGate.BALANCED
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    status: AgentStatus = AgentStatus.IDLE
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3


@dataclass
class AgentConfig:
    """Configuration for AI agents"""
    agent_id: str
    agent_type: str
    enabled: bool = True
    priority: AgentPriority = AgentPriority.MEDIUM
    quality_gate: QualityGate = QualityGate.BALANCED
    max_concurrent_tasks: int = 3
    timeout_seconds: int = 300
    retry_policy: Dict[str, Any] = field(default_factory=lambda: {
        'max_retries': 3,
        'backoff_multiplier': 2,
        'initial_delay': 1
    })
    routing_rules: List[Dict[str, Any]] = field(default_factory=list)
    cost_limits: Dict[str, float] = field(default_factory=lambda: {
        'daily_limit': 50.0,
        'task_limit': 5.0
    })


class BaseAgent(ABC):
    """Base class for AI agents"""
    
    def __init__(self, config: AgentConfig, souls_manager: SoulsManager,
                 openrouter: OpenRouterIntegration, content_pipeline: ContentPipeline):
        self.config = config
        self.souls_manager = souls_manager
        self.openrouter = openrouter
        self.content_pipeline = content_pipeline
        self.logger = LoggingUtils.setup_logger(f"{self.__class__.__name__}")
        
        self.status = AgentStatus.IDLE
        self.current_tasks: Dict[str, AgentTask] = {}
        self.completed_tasks: List[AgentTask] = []
        self.execution_stats = {
            'total_executions': 0,
            'successful_executions': 0,
            'failed_executions': 0,
            'total_execution_time': 0.0,
            'average_execution_time': 0.0
        }
    
    @abstractmethod
    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """Execute a specific task - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def get_routing_rules(self) -> List[Dict[str, Any]]:
        """Get routing rules for this agent type"""
        pass
    
    def apply_quality_gate(self, task: AgentTask, result: Dict[str, Any]) -> bool:
        """Apply quality gate validation to task results"""
        quality_gate = task.quality_gate
        
        # Basic validation that applies to all quality gates
        if not result or 'error' in result:
            if quality_gate != QualityGate.EXPERIMENTAL:
                return False
        
        # Strict quality gate - additional validation
        if quality_gate == QualityGate.STRICT:
            if 'content' in result and len(result.get('content', '')) < 50:
                return False
            if 'cost_estimate' in result and result['cost_estimate'] > 10.0:
                return False
        
        # Experimental quality gate - always pass
        if quality_gate == QualityGate.EXPERIMENTAL:
            return True
        
        return True
    
    def apply_routing_rules(self, task: AgentTask) -> bool:
        """Apply routing rules to determine if task should be executed"""
        for rule in self.config.routing_rules:
            # Check if rule applies to this task
            if self._rule_matches(rule, task):
                # Apply rule action
                action = rule.get('action', 'allow')
                if action == 'deny':
                    self.logger.info(f"Task {task.task_id} denied by routing rule")
                    return False
                elif action == 'modify':
                    self._apply_rule_modifications(rule, task)
        
        return True
    
    def _rule_matches(self, rule: Dict[str, Any], task: AgentTask) -> bool:
        """Check if a routing rule matches the task"""
        conditions = rule.get('conditions', {})
        
        # Check priority condition
        if 'priority' in conditions:
            if task.priority.value != conditions['priority']:
                return False
        
        # Check agent type condition
        if 'agent_type' in conditions:
            if task.agent_type != conditions['agent_type']:
                return False
        
        # Check data conditions
        if 'data_conditions' in conditions:
            for key, value in conditions['data_conditions'].items():
                if task.data.get(key) != value:
                    return False
        
        return True
    
    def _apply_rule_modifications(self, rule: Dict[str, Any], task: AgentTask):
        """Apply modifications from routing rule to task"""
        modifications = rule.get('modifications', {})
        
        if 'quality_gate' in modifications:
            task.quality_gate = QualityGate(modifications['quality_gate'])
        
        if 'priority' in modifications:
            task.priority = AgentPriority(modifications['priority'])
        
        if 'timeout' in modifications:
            self.config.timeout_seconds = modifications['timeout']
    
    async def run_task(self, task: AgentTask) -> Dict[str, Any]:
        """Run a task with full agent framework features"""
        task.status = AgentStatus.RUNNING
        task.started_at = datetime.now().isoformat()
        self.current_tasks[task.task_id] = task
        
        try:
            # Apply routing rules
            if not self.apply_routing_rules(task):
                task.status = AgentStatus.COMPLETED
                task.completed_at = datetime.now().isoformat()
                return {'status': 'denied_by_routing_rules'}
            
            # Execute task
            self.logger.info(f"Executing task {task.task_id} with agent {self.config.agent_id}")
            result = await self.execute_task(task)
            
            # Apply quality gate
            if not self.apply_quality_gate(task, result):
                raise Exception("Quality gate validation failed")
            
            # Update task status
            task.status = AgentStatus.COMPLETED
            task.completed_at = datetime.now().isoformat()
            task.result = result
            
            # Update stats
            self.execution_stats['total_executions'] += 1
            self.execution_stats['successful_executions'] += 1
            
            # Calculate execution time
            if task.started_at:
                execution_time = (datetime.fromisoformat(task.completed_at) - 
                               datetime.fromisoformat(task.started_at)).total_seconds()
                self.execution_stats['total_execution_time'] += execution_time
                self.execution_stats['average_execution_time'] = (
                    self.execution_stats['total_execution_time'] / 
                    self.execution_stats['total_executions']
                )
            
            self.logger.info(f"Task {task.task_id} completed successfully")
            return result
            
        except Exception as e:
            # Handle failure with retry policy
            task.error = str(e)
            task.retry_count += 1
            
            if task.retry_count < task.max_retries:
                self.logger.warning(f"Task {task.task_id} failed, retrying ({task.retry_count}/{task.max_retries})")
                
                # Apply backoff
                retry_policy = self.config.retry_policy
                delay = retry_policy['initial_delay'] * (
                    retry_policy['backoff_multiplier'] ** (task.retry_count - 1)
                )
                await asyncio.sleep(delay)
                
                # Retry task
                return await self.run_task(task)
            else:
                # Max retries reached
                task.status = AgentStatus.ERROR
                task.completed_at = datetime.now().isoformat()
                self.execution_stats['total_executions'] += 1
                self.execution_stats['failed_executions'] += 1
                
                self.logger.error(f"Task {task.task_id} failed after {task.max_retries} retries: {e}")
                raise
        
        finally:
            # Move to completed tasks
            if task.task_id in self.current_tasks:
                del self.current_tasks[task.task_id]
            self.completed_tasks.append(task)


class ContentGenerationAgent(BaseAgent):
    """Agent for autonomous content generation"""
    
    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """Execute content generation task"""
        soul_id = task.data.get('soul_id')
        platform = task.data.get('platform')
        content_type = task.data.get('content_type', 'post')
        
        if not soul_id or not platform:
            raise ValueError("soul_id and platform required for content generation")
        
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            raise ValueError(f"Soul {soul_id} not found")
        
        from .openrouter_integration import ContentRequest
        request = ContentRequest(
            soul_id=soul_id,
            platform=platform,
            content_type=content_type,
            context=task.data.get('context'),
            tone=task.data.get('tone'),
            length=task.data.get('length', 'medium')
        )
        
        generated = self.openrouter.generate_soul_content(soul, request)
        
        return {
            'content': generated.content,
            'model_used': generated.model_used,
            'tokens_used': generated.tokens_used,
            'cost_estimate': generated.cost_estimate,
            'metadata': generated.metadata
        }
    
    def get_routing_rules(self) -> List[Dict[str, Any]]:
        """Get routing rules for content generation"""
        return [
            {
                'conditions': {
                    'priority': 'critical',
                    'data_conditions': {'rarity': 'Legendary'}
                },
                'action': 'modify',
                'modifications': {
                    'quality_gate': 'strict',
                    'timeout': 600
                }
            },
            {
                'conditions': {
                    'data_conditions': {'content_type': 'bulk'}
                },
                'action': 'modify',
                'modifications': {
                    'quality_gate': 'fast'
                }
            }
        ]


class CampaignManagementAgent(BaseAgent):
    """Agent for managing content campaigns"""
    
    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """Execute campaign management task"""
        campaign_name = task.data.get('campaign_name', 'Autonomous Campaign')
        soul_ids = task.data.get('soul_ids', [])
        platforms = task.data.get('platforms', [])
        content_types = task.data.get('content_types', ['post'])
        timeline_days = task.data.get('timeline_days', 7)
        
        if not soul_ids or not platforms:
            raise ValueError("soul_ids and platforms required for campaign")
        
        results = self.content_pipeline.generate_campaign(
            campaign_name, soul_ids, platforms, content_types, timeline_days
        )
        
        return results
    
    def get_routing_rules(self) -> List[Dict[str, Any]]:
        """Get routing rules for campaign management"""
        return [
            {
                'conditions': {
                    'priority': 'critical'
                },
                'action': 'modify',
                'modifications': {
                    'quality_gate': 'strict',
                    'timeout': 900
                }
            }
        ]


class PipelineOptimizationAgent(BaseAgent):
    """Agent for optimizing content pipeline performance"""
    
    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """Execute pipeline optimization task"""
        optimization = self.content_pipeline.optimize_pipeline()
        
        # Apply recommended optimizations if task specifies auto-apply
        if task.data.get('auto_apply', False):
            self._apply_optimizations(optimization['recommendations'])
        
        return optimization
    
    def _apply_optimizations(self, recommendations: List[Dict[str, Any]]):
        """Apply optimization recommendations"""
        for rec in recommendations:
            if rec['type'] == 'cost':
                # Switch to more cost-effective models
                self.openrouter.config['default_model'] = 'gemini-2-5-flash'
            elif rec['type'] == 'activity':
                # Schedule content for inactive souls
                self.content_pipeline.generate_due_content()
    
    def get_routing_rules(self) -> List[Dict[str, Any]]:
        """Get routing rules for pipeline optimization"""
        return [
            {
                'conditions': {
                    'priority': 'low'
                },
                'action': 'modify',
                'modifications': {
                    'quality_gate': 'fast'
                }
            }
        ]


class AnalyticsAgent(BaseAgent):
    """Agent for analytics and monitoring"""
    
    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """Execute analytics task"""
        analysis_type = task.data.get('analysis_type', 'general')
        
        if analysis_type == 'pipeline':
            return self.content_pipeline.get_pipeline_statistics()
        elif analysis_type == 'cost':
            return self.openrouter.get_usage_statistics()
        elif analysis_type == 'souls':
            return self.souls_manager.get_statistics()
        else:
            # General analytics
            return {
                'pipeline': self.content_pipeline.get_pipeline_statistics(),
                'cost': self.openrouter.get_usage_statistics(),
                'souls': self.souls_manager.get_statistics()
            }
    
    def get_routing_rules(self) -> List[Dict[str, Any]]:
        """Get routing rules for analytics"""
        return [
            {
                'conditions': {
                    'data_conditions': {'analysis_type': 'cost'}
                },
                'action': 'modify',
                'modifications': {
                    'quality_gate': 'fast'
                }
            }
        ]


class AgentOrchestrator:
    """
    Orchestrates multiple AI agents with task scheduling and routing
    """
    
    def __init__(self, souls_manager: SoulsManager, openrouter: OpenRouterIntegration,
                 content_pipeline: ContentPipeline, config_path: Optional[str] = None):
        self.souls_manager = souls_manager
        self.openrouter = openrouter
        self.content_pipeline = content_pipeline
        self.logger = LoggingUtils.setup_logger(__name__)
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize agents
        self.agents: Dict[str, BaseAgent] = {}
        self._initialize_agents()
        
        # Task queue
        self.task_queue: List[AgentTask] = []
        self.completed_tasks: List[AgentTask] = []
        
        # Running state
        self.is_running = False
        self.max_concurrent_tasks = self.config.get('max_concurrent_tasks', 5)
        
        self.logger.info("Agent Orchestrator initialized")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load orchestrator configuration"""
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / 'config' / 'agent_config.json'
        
        config_file = Path(config_path)
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Failed to load agent config: {e}, using defaults")
        
        return {
            'max_concurrent_tasks': 5,
            'task_timeout': 300,
            'enable_auto_scaling': True,
            'cost_management': {
                'daily_limit': 100.0,
                'alert_threshold': 0.8
            }
        }
    
    def _initialize_agents(self):
        """Initialize all available agents"""
        agent_configs = [
            AgentConfig(
                agent_id='content_generator',
                agent_type='content_generation',
                priority=AgentPriority.HIGH,
                quality_gate=QualityGate.BALANCED
            ),
            AgentConfig(
                agent_id='campaign_manager',
                agent_type='campaign_management',
                priority=AgentPriority.MEDIUM,
                quality_gate=QualityGate.STRICT
            ),
            AgentConfig(
                agent_id='pipeline_optimizer',
                agent_type='pipeline_optimization',
                priority=AgentPriority.LOW,
                quality_gate=QualityGate.FAST
            ),
            AgentConfig(
                agent_id='analytics',
                agent_type='analytics',
                priority=AgentPriority.LOW,
                quality_gate=QualityGate.FAST
            )
        ]
        
        for config in agent_configs:
            if config.agent_type == 'content_generation':
                agent = ContentGenerationAgent(config, self.souls_manager, 
                                             self.openrouter, self.content_pipeline)
            elif config.agent_type == 'campaign_management':
                agent = CampaignManagementAgent(config, self.souls_manager,
                                               self.openrouter, self.content_pipeline)
            elif config.agent_type == 'pipeline_optimization':
                agent = PipelineOptimizationAgent(config, self.souls_manager,
                                                 self.openrouter, self.content_pipeline)
            elif config.agent_type == 'analytics':
                agent = AnalyticsAgent(config, self.souls_manager,
                                      self.openrouter, self.content_pipeline)
            else:
                continue
            
            self.agents[config.agent_id] = agent
        
        self.logger.info(f"Initialized {len(self.agents)} agents")
    
    def submit_task(self, task: AgentTask) -> str:
        """Submit a task to the orchestrator"""
        # Find appropriate agent
        agent = self.agents.get(task.agent_type)
        if not agent:
            raise ValueError(f"Agent type {task.agent_type} not found")
        
        # Add to queue
        self.task_queue.append(task)
        self.logger.info(f"Task {task.task_id} submitted to queue")
        
        return task.task_id
    
    async def process_tasks(self):
        """Process tasks from the queue"""
        self.is_running = True
        
        while self.is_running and self.task_queue:
            # Check concurrent task limit
            running_tasks = sum(1 for agent in self.agents.values() 
                             if agent.status == AgentStatus.RUNNING)
            
            if running_tasks >= self.max_concurrent_tasks:
                await asyncio.sleep(1)
                continue
            
            # Get next task (sorted by priority)
            self.task_queue.sort(key=lambda t: t.priority.value, reverse=True)
            task = self.task_queue.pop(0)
            
            # Find appropriate agent
            agent = self.agents.get(task.agent_type)
            if not agent:
                self.logger.error(f"No agent found for task type {task.agent_type}")
                continue
            
            # Execute task
            try:
                result = await agent.run_task(task)
                self.completed_tasks.append(task)
            except Exception as e:
                self.logger.error(f"Task {task.task_id} failed: {e}")
                task.status = AgentStatus.ERROR
                task.error = str(e)
                self.completed_tasks.append(task)
        
        self.is_running = False
    
    def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get overall orchestrator status"""
        agent_statuses = {}
        for agent_id, agent in self.agents.items():
            agent_statuses[agent_id] = {
                'status': agent.status.value,
                'current_tasks': len(agent.current_tasks),
                'completed_tasks': len(agent.completed_tasks),
                'execution_stats': agent.execution_stats
            }
        
        return {
            'is_running': self.is_running,
            'queue_length': len(self.task_queue),
            'completed_tasks': len(self.completed_tasks),
            'max_concurrent_tasks': self.max_concurrent_tasks,
            'agent_statuses': agent_statuses,
            'config': self.config
        }
    
    def shutdown(self):
        """Shutdown the orchestrator gracefully"""
        self.is_running = False
        self.logger.info("Agent Orchestrator shutdown complete")