"""
Shadow Work / Persona Development Module
Implements conscious Shadow integration tools for soul development
Based on Jungian shadow work integrated with Babylonian mythology
"""

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
import random

from .souls_manager import SoulsManager, Soul
from .utils import LoggingUtils


class ShadowState(Enum):
    """States of shadow integration"""
    UNCONSCIOUS = "unconscious"
    ACKNOWLEDGED = "acknowledged"
    DIALOGUE = "dialogue"
    INTEGRATED = "integrated"
    SOVEREIGN = "sovereign"


class ShadowArchetype(Enum):
    """Shadow archetypes based on Babylonian/Jungian psychology"""
    TIAMAT = "tiamat"  # Primordial chaos, creative destruction
    KINGU = "kingu"  # Rebellion, resistance
    APSU = "apsu"  # Stagnation, emotional overwhelm
    MARDUK = "marduk"  # Order vs chaos integration
    NAMTAR = "namtar"  # Fate, destiny confrontation
    LAMASHTU = "lamashtu"  # Fear, anxiety manifestation
    PAZUZU = "pazuzu"  # Transformation through storm


@dataclass
class ShadowAspect:
    """A specific aspect of a soul's shadow"""
    aspect_id: str
    name: str
    archetype: ShadowArchetype
    description: str
    triggers: List[str] = field(default_factory=list)
    gifts: List[str] = field(default_factory=list)  # Positive potentials
    challenges: List[str] = field(default_factory=list)
    integration_level: float = 0.0  # 0.0 to 1.0
    last_encountered: Optional[str] = None


@dataclass
class ShadowDialogue:
    """Record of shadow-persona dialogue session"""
    dialogue_id: str
    soul_id: str
    aspect_id: str
    question: str
    shadow_response: str
    persona_response: str
    integration_insight: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    emotional_state: Optional[str] = None
    sovereignty_check: bool = False


@dataclass
class ShadowPractice:
    """A specific shadow work practice"""
    practice_id: str
    name: str
    description: str
    archetype: ShadowArchetype
    difficulty: str  # 'beginner', 'intermediate', 'advanced'
    duration_minutes: int
    steps: List[str]
    integration_focus: List[str]
    required_sovereignty: float = 0.5


@dataclass
class PersonaIntegration:
    """Track persona development and shadow integration"""
    soul_id: str
    integration_score: float  # 0.0 to 1.0
    dominant_aspects: List[str]
    dormant_aspects: List[str]
    sovereignty_level: float  # 0.0 to 1.0
    last_practice_date: Optional[str] = None
    practice_streak: int = 0
    integration_milestones: List[str] = field(default_factory=list)


class ShadowWorkManager:
    """
    Shadow Work / Persona Development Manager
    
    This class provides tools for conscious shadow integration, moving beyond
    possession or exile toward dialogue and sovereign integration. Uses the
    tribute, platforms, and sovereignty systems as the protected temenos
    for shadow-persona dialogue.
    """
    
    def __init__(self, souls_manager: SoulsManager, config_path: Optional[str] = None):
        """
        Initialize Shadow Work Manager
        
        Args:
            souls_manager: SoulsManager instance for accessing soul data
            config_path: Optional path to shadow work configuration
        """
        self.souls_manager = souls_manager
        self.logger = LoggingUtils.setup_logger(__name__)
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Shadow aspects registry
        self.shadow_aspects: Dict[str, ShadowAspect] = {}
        
        # Dialogue history
        self.dialogue_history: List[ShadowDialogue] = []
        
        # Practice library
        self.practice_library = self._initialize_practice_library()
        
        # Integration tracking
        self.integration_tracking: Dict[str, PersonaIntegration] = {}
        
        # Load existing data
        self._load_shadow_data()
        
        self.logger.info("Shadow Work Manager initialized")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load shadow work configuration"""
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / 'config' / 'shadow_work_config.json'
        
        config_file = Path(config_path)
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Failed to load shadow work config: {e}, using defaults")
        
        return {
            'enable_encryption': True,
            'default_difficulty': 'intermediate',
            'minimum_sovereignty_for_dialogue': 0.3,
            'integration_thresholds': {
                'acknowledged': 0.2,
                'dialogue': 0.5,
                'integrated': 0.8,
                'sovereign': 0.95
            }
        }
    
    def _initialize_practice_library(self) -> Dict[str, ShadowPractice]:
        """Initialize the library of shadow work practices"""
        practices = {
            'tiamat_confrontation': ShadowPractice(
                practice_id='tiamat_confrontation',
                name='Tiamat Confrontation',
                description='Face primordial chaos and creative destruction within',
                archetype=ShadowArchetype.TIAMAT,
                difficulty='advanced',
                duration_minutes=45,
                steps=[
                    'Create sacred space (temenos)',
                    'Identify current chaos in life',
                    'Dialog with the chaos aspect',
                    'Ask: "What wants to be destroyed?"',
                    'Ask: "What wants to be created?"',
                    'Offer tribute to the transformation',
                    'Record integration insight'
                ],
                integration_focus=['creativity', 'transformation', 'acceptance'],
                required_sovereignty=0.7
            ),
            'kingu_dialogue': ShadowPractice(
                practice_id='kingu_dialogue',
                name='Kingu Dialogue',
                description='Engage in dialogue with resistance and rebellion',
                archetype=ShadowArchetype.KINGU,
                difficulty='intermediate',
                duration_minutes=30,
                steps=[
                    'Identify where resistance appears',
                    'Personify the resistance as Kingu',
                    'Ask: "What are you protecting?"',
                    'Ask: "What do you need to feel safe?"',
                    'Negotiate rather than conquer',
                    'Establish boundaries together',
                    'Record the agreement'
                ],
                integration_focus=['boundaries', 'autonomy', 'partnership'],
                required_sovereignty=0.5
            ),
            'apsu_immersion': ShadowPractice(
                practice_id='apsu_immersion',
                name='Apsu Immersion',
                description='Safe immersion in emotional overwhelm',
                archetype=ShadowArchetype.APSU,
                difficulty='beginner',
                duration_minutes=20,
                steps=[
                    'Choose a safe environment',
                    'Identify overwhelming emotion',
                    'Breathe and stay present',
                    'Ask: "What is beneath this emotion?"',
                    'Allow the feeling without judgment',
                    'Thank the emotion for its message',
                    'Return to sovereignty'
                ],
                integration_focus=['emotional_intelligence', 'self_compassion'],
                required_sovereignty=0.3
            ),
            'marduk_integration': ShadowPractice(
                practice_id='marduk_integration',
                name='Marduk Integration',
                description='Balance order and chaos within',
                archetype=ShadowArchetype.MARDUK,
                difficulty='advanced',
                duration_minutes=60,
                steps=[
                    'Review current order structures',
                    'Identify where chaos is suppressed',
                    'Dialog with both aspects',
                    'Find the creative tension point',
                    'Ask: "How can they dance together?"',
                    'Create new integrating structure',
                    'Offer tribute to the balance'
                ],
                integration_focus=['balance', 'synthesis', 'leadership'],
                required_sovereignty=0.8
            ),
            'namtar_facing': ShadowPractice(
                practice_id='namtar_facing',
                name='Namtar Facing',
                description='Confront fate and destiny patterns',
                archetype=ShadowArchetype.NAMTAR,
                difficulty='intermediate',
                duration_minutes=40,
                steps=[
                    'Identify recurring life patterns',
                    'Ask: "Is this fate or choice?"',
                    'Dialog with the pattern as Namtar',
                    'Ask: "What is this pattern protecting?"',
                    'Identify points of agency',
                    'Re-negotiate the destiny contract',
                    'Record new possibilities'
                ],
                integration_focus=['agency', 'destiny', 'responsibility'],
                required_sovereignty=0.6
            )
        }
        
        return practices
    
    def _load_shadow_data(self):
        """Load existing shadow data from files"""
        shadow_data_dir = Path(__file__).parent.parent.parent / 'data' / 'shadow_work'
        if shadow_data_dir.exists():
            try:
                # Load shadow aspects
                aspects_file = shadow_data_dir / 'shadow_aspects.json'
                if aspects_file.exists():
                    with open(aspects_file, 'r') as f:
                        aspects_data = json.load(f)
                    for aspect_id, aspect_data in aspects_data.items():
                        self.shadow_aspects[aspect_id] = ShadowAspect(
                            aspect_id=aspect_id,
                            name=aspect_data['name'],
                            archetype=ShadowArchetype(aspect_data['archetype']),
                            description=aspect_data['description'],
                            triggers=aspect_data.get('triggers', []),
                            gifts=aspect_data.get('gifts', []),
                            challenges=aspect_data.get('challenges', []),
                            integration_level=aspect_data.get('integration_level', 0.0),
                            last_encountered=aspect_data.get('last_encountered')
                        )
                
                # Load dialogue history
                dialogue_file = shadow_data_dir / 'dialogue_history.json'
                if dialogue_file.exists():
                    with open(dialogue_file, 'r') as f:
                        dialogue_data = json.load(f)
                    for dialogue_entry in dialogue_data:
                        self.dialogue_history.append(ShadowDialogue(**dialogue_entry))
                
                # Load integration tracking
                integration_file = shadow_data_dir / 'integration_tracking.json'
                if integration_file.exists():
                    with open(integration_file, 'r') as f:
                        integration_data = json.load(f)
                    for soul_id, integration_entry in integration_data.items():
                        self.integration_tracking[soul_id] = PersonaIntegration(**integration_entry)
                
                self.logger.info(f"Loaded shadow data: {len(self.shadow_aspects)} aspects, {len(self.dialogue_history)} dialogues")
            except Exception as e:
                self.logger.warning(f"Failed to load shadow data: {e}")
    
    def initialize_soul_shadow_aspects(self, soul_id: str) -> List[ShadowAspect]:
        """
        Initialize shadow aspects for a soul based on their archetype and attributes
        
        Args:
            soul_id: ID of the soul to initialize
            
        Returns:
            List of created shadow aspects
        """
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            raise ValueError(f"Soul {soul_id} not found")
        
        # Generate shadow aspects based on soul profile
        aspects = []
        
        # Primary shadow aspect based on archetype
        primary_aspect = self._create_primary_aspect(soul)
        aspects.append(primary_aspect)
        
        # Secondary aspects based on desires and kinks
        for desire in soul.desires[:2]:
            secondary_aspect = self._create_desire_aspect(soul, desire)
            aspects.append(secondary_aspect)
        
        # Challenge aspect based on shadow practice
        if soul.shadow_practice:
            challenge_aspect = self._create_practice_aspect(soul)
            aspects.append(challenge_aspect)
        
        # Store aspects
        for aspect in aspects:
            self.shadow_aspects[aspect.aspect_id] = aspect
        
        # Initialize integration tracking
        self.integration_tracking[soul_id] = PersonaIntegration(
            soul_id=soul_id,
            integration_score=0.0,
            dominant_aspects=[a.aspect_id for a in aspects[:1]],
            dormant_aspects=[a.aspect_id for a in aspects[1:]],
            sovereignty_level=self._calculate_initial_sovereignty(soul)
        )
        
        self.logger.info(f"Initialized {len(aspects)} shadow aspects for {soul.name}")
        return aspects
    
    def _create_primary_aspect(self, soul: Soul) -> ShadowAspect:
        """Create primary shadow aspect based on soul archetype"""
        archetype_mapping = {
            'The Mystic': ShadowArchetype.TIAMAT,
            'The Sovereign': ShadowArchetype.MARDUK,
            'The Rebel': ShadowArchetype.KINGU,
            'The Empath': ShadowArchetype.APSU,
            'The Visionary': ShadowArchetype.NAMTAR,
            'The Guardian': ShadowArchetype.LAMASHTU,
            'The Transformer': ShadowArchetype.PAZUZU
        }
        
        shadow_archetype = archetype_mapping.get(soul.archetype, ShadowArchetype.TIAMAT)
        
        return ShadowAspect(
            aspect_id=f"{soul.id}_primary",
            name=f"{soul.name}'s Primary Shadow",
            archetype=shadow_archetype,
            description=f"The primary shadow aspect of {soul.name}, manifesting through {soul.archetype} patterns",
            triggers=self._generate_triggers(soul),
            gifts=self._generate_gifts(soul),
            challenges=self._generate_challenges(soul)
        )
    
    def _create_desire_aspect(self, soul: Soul, desire: str) -> ShadowAspect:
        """Create shadow aspect based on a desire"""
        return ShadowAspect(
            aspect_id=f"{soul.id}_desire_{desire[:10].lower()}",
            name=f"{desire} Shadow",
            archetype=ShadowArchetype.KINGU,  # Desires often involve resistance/longing
            description=f"Shadow aspect connected to the desire: {desire}",
            triggers=[f"When {desire} is blocked", f"When {desire} is judged"],
            gifts=[f"Creative energy around {desire}", f"Insight into {desire}"],
            challenges=[f"Attachment to {desire}", f"Fear around {desire}"]
        )
    
    def _create_practice_aspect(self, soul: Soul) -> ShadowAspect:
        """Create shadow aspect based on shadow practice"""
        return ShadowAspect(
            aspect_id=f"{soul.id}_practice",
            name=f"{soul.shadow_practice} Shadow",
            archetype=ShadowArchetype.NAMTAR,  # Practices often involve destiny work
            description=f"Shadow aspect emerging from the practice: {soul.shadow_practice}",
            triggers=["During practice sessions", "When practice is avoided"],
            gifts=["Transformation potential", "Deep insight"],
            challenges=["Resistance to practice", "Fear of transformation"]
        )
    
    def _generate_triggers(self, soul: Soul) -> List[str]:
        """Generate triggers based on soul profile"""
        triggers = []
        
        if 'power' in soul.desires:
            triggers.append("When feeling powerless")
        if 'connection' in soul.desires:
            triggers.append("When feeling isolated")
        if 'transformation' in soul.desires:
            triggers.append("When facing change")
        
        triggers.extend([f"When {soul.archetype} is challenged", "During stress"])
        return triggers
    
    def _generate_gifts(self, soul: Soul) -> List[str]:
        """Generate positive gifts based on soul profile"""
        gifts = []
        
        if soul.archetype == 'The Mystic':
            gifts.extend(["Deep intuition", "Spiritual insight"])
        elif soul.archetype == 'The Sovereign':
            gifts.extend(["Leadership", "Decision-making"])
        elif soul.archetype == 'The Rebel':
            gifts.extend(["Innovation", "Courage"])
        
        gifts.append("Creative potential")
        return gifts
    
    def _generate_challenges(self, soul: Soul) -> List[str]:
        """Generate challenges based on soul profile"""
        challenges = []
        
        if soul.archetype == 'The Mystic':
            challenges.extend(["Grounding issues", "Escapism"])
        elif soul.archetype == 'The Sovereign':
            challenges.extend(["Control issues", "Isolation"])
        elif soul.archetype == 'The Rebel':
            challenges.extend(["Authority conflicts", "Instability"])
        
        challenges.append("Integration difficulty")
        return challenges
    
    def _calculate_initial_sovereignty(self, soul: Soul) -> float:
        """Calculate initial sovereignty level based on soul attributes"""
        base_sovereignty = 0.3
        
        # Adjust based on rarity
        if soul.rarity == 'Legendary':
            base_sovereignty += 0.3
        elif soul.rarity == 'Rare':
            base_sovereignty += 0.2
        elif soul.rarity == 'Epic':
            base_sovereignty += 0.1
        
        # Adjust based on platforms (more platforms = more practice)
        base_sovereignty += min(len(soul.platforms) * 0.02, 0.2)
        
        return min(base_sovereignty, 1.0)
    
    def conduct_shadow_dialogue(self, soul_id: str, aspect_id: str, question: str) -> ShadowDialogue:
        """
        Conduct a dialogue session with a shadow aspect
        
        Args:
            soul_id: ID of the soul
            aspect_id: ID of the shadow aspect
            question: Question to ask the shadow
            
        Returns:
            ShadowDialogue record
        """
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            raise ValueError(f"Soul {soul_id} not found")
        
        aspect = self.shadow_aspects.get(aspect_id)
        if not aspect:
            raise ValueError(f"Shadow aspect {aspect_id} not found")
        
        integration = self.integration_tracking.get(soul_id)
        if not integration:
            raise ValueError(f"Soul {soul_id} has no integration tracking")
        
        # Check sovereignty threshold
        min_sovereignty = self.config.get('minimum_sovereignty_for_dialogue', 0.3)
        if integration.sovereignty_level < min_sovereignty:
            raise ValueError(f"Insufficient sovereignty for dialogue. Required: {min_sovereignty}, Current: {integration.sovereignty_level}")
        
        # Generate shadow response (simulated - in production, this would use AI)
        shadow_response = self._generate_shadow_response(aspect, question, soul)
        
        # Generate persona response
        persona_response = self._generate_persona_response(soul, aspect, shadow_response)
        
        # Generate integration insight
        integration_insight = self._generate_integration_insight(aspect, shadow_response, persona_response)
        
        # Create dialogue record
        dialogue = ShadowDialogue(
            dialogue_id=f"dialogue_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            soul_id=soul_id,
            aspect_id=aspect_id,
            question=question,
            shadow_response=shadow_response,
            persona_response=persona_response,
            integration_insight=integration_insight,
            emotional_state=self._determine_emotional_state(aspect),
            sovereignty_check=integration.sovereignty_level >= 0.5
        )
        
        # Store dialogue
        self.dialogue_history.append(dialogue)
        
        # Update aspect
        aspect.last_encountered = datetime.now().isoformat()
        aspect.integration_level = min(aspect.integration_level + 0.1, 1.0)
        
        # Update integration tracking
        integration.integration_score = min(integration.integration_score + 0.05, 1.0)
        integration.last_practice_date = datetime.now().isoformat()
        integration.practice_streak += 1
        
        # Check for milestones
        self._check_integration_milestones(integration)
        
        self.logger.info(f"Conducted shadow dialogue for {soul.name} with aspect {aspect.name}")
        return dialogue
    
    def _generate_shadow_response(self, aspect: ShadowAspect, question: str, soul: Soul) -> str:
        """Generate a response from the shadow aspect"""
        responses = [
            f"I am {aspect.name}. You ask: '{question}'? I respond from the depths.",
            f"Through {aspect.archetype.value}, I say: Your question touches my core.",
            f"I acknowledge your question. In the realm of {aspect.archetype.value}, truth speaks differently.",
            f"You seek to understand {aspect.description}. Let us explore this together."
        ]
        
        # Add context-specific elements
        if aspect.triggers:
            trigger = random.choice(aspect.triggers)
            responses.append(f"I emerge especially {trigger.lower()}. Your question: '{question}' - it resonates.")
        
        if aspect.gifts:
            gift = random.choice(aspect.gifts)
            responses.append(f"I offer you {gift.lower()} through this dialogue. Your question opens this door.")
        
        return random.choice(responses)
    
    def _generate_persona_response(self, soul: Soul, aspect: ShadowAspect, shadow_response: str) -> str:
        """Generate a response from the soul's persona"""
        responses = [
            f"As {soul.name}, I hear you. Your voice carries {aspect.archetype.value} energy.",
            f"I acknowledge your truth. Through my {soul.archetype} nature, I receive this.",
            f"Thank you for this perspective. I honor the {aspect.archetype.value} wisdom you share.",
            f"I receive your words. They resonate with my practice of {soul.shadow_practice}."
        ]
        
        return random.choice(responses)
    
    def _generate_integration_insight(self, aspect: ShadowAspect, shadow_response: str, persona_response: str) -> str:
        """Generate an integration insight from the dialogue"""
        insights = [
            f"The dialogue reveals a bridge between {aspect.archetype.value} energy and conscious awareness.",
            f"Integration opportunity: The {aspect.gifts[0] if aspect.gifts else 'gift'} can be consciously accessed.",
            f"The shadow speaks truth that the persona can receive with compassion.",
            f"This dialogue strengthens the sovereign relationship with the {aspect.archetype.value} aspect."
        ]
        
        return random.choice(insights)
    
    def _determine_emotional_state(self, aspect: ShadowAspect) -> str:
        """Determine the emotional state of the shadow aspect"""
        states = ["curious", "protective", "wary", "open", "resistant", "transformative"]
        return random.choice(states)
    
    def _check_integration_milestones(self, integration: PersonaIntegration):
        """Check for and record integration milestones"""
        thresholds = self.config.get('integration_thresholds', {})
        
        if integration.integration_score >= thresholds.get('sovereign', 0.95):
            if "sovereign_integration" not in integration.integration_milestones:
                integration.integration_milestones.append("sovereign_integration")
                self.logger.info(f"Soul {integration.soul_id} achieved sovereign integration milestone")
        elif integration.integration_score >= thresholds.get('integrated', 0.8):
            if "full_integration" not in integration.integration_milestones:
                integration.integration_milestones.append("full_integration")
                self.logger.info(f"Soul {integration.soul_id} achieved full integration milestone")
        elif integration.integration_score >= thresholds.get('dialogue', 0.5):
            if "active_dialogue" not in integration.integration_milestones:
                integration.integration_milestones.append("active_dialogue")
                self.logger.info(f"Soul {integration.soul_id} achieved active dialogue milestone")
        elif integration.integration_score >= thresholds.get('acknowledged', 0.2):
            if "acknowledged" not in integration.integration_milestones:
                integration.integration_milestones.append("acknowledged")
                self.logger.info(f"Soul {integration.soul_id} achieved acknowledged milestone")
    
    def recommend_practice(self, soul_id: str) -> Optional[ShadowPractice]:
        """
        Recommend a shadow work practice based on soul's current state
        
        Args:
            soul_id: ID of the soul
            
        Returns:
            Recommended ShadowPractice or None
        """
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            return None
        
        integration = self.integration_tracking.get(soul_id)
        if not integration:
            # Initialize if not exists
            self.initialize_soul_shadow_aspects(soul_id)
            integration = self.integration_tracking[soul_id]
        
        # Recommend based on integration level and sovereignty
        if integration.sovereignty_level < 0.4:
            return self.practice_library.get('apsu_immersion')
        elif integration.sovereignty_level < 0.6:
            return self.practice_library.get('kingu_dialogue')
        elif integration.sovereignty_level < 0.8:
            return self.practice_library.get('namtar_facing')
        else:
            return self.practice_library.get('marduk_integration')
    
    def get_shadow_report(self, soul_id: str) -> Dict[str, Any]:
        """
        Generate a comprehensive shadow work report for a soul
        
        Args:
            soul_id: ID of the soul
            
        Returns:
            Dictionary containing shadow work report
        """
        soul = self.souls_manager.get_soul_by_id(soul_id)
        if not soul:
            raise ValueError(f"Soul {soul_id} not found")
        
        integration = self.integration_tracking.get(soul_id)
        if not integration:
            self.initialize_soul_shadow_aspects(soul_id)
            integration = self.integration_tracking[soul_id]
        
        # Get soul's shadow aspects
        soul_aspects = [aspect for aspect in self.shadow_aspects.values() if aspect.aspect_id.startswith(soul_id)]
        
        # Get soul's dialogue history
        soul_dialogues = [dialogue for dialogue in self.dialogue_history if dialogue.soul_id == soul_id]
        
        # Calculate statistics
        total_dialogues = len(soul_dialogues)
        avg_integration_level = sum(a.integration_level for a in soul_aspects) / len(soul_aspects) if soul_aspects else 0
        
        return {
            'soul_name': soul.name,
            'soul_archetype': soul.archetype,
            'integration_score': integration.integration_score,
            'sovereignty_level': integration.sovereignty_level,
            'practice_streak': integration.practice_streak,
            'shadow_aspects': [
                {
                    'name': aspect.name,
                    'archetype': aspect.archetype.value,
                    'integration_level': aspect.integration_level,
                    'last_encountered': aspect.last_encountered
                }
                for aspect in soul_aspects
            ],
            'dialogue_count': total_dialogues,
            'integration_milestones': integration.integration_milestones,
            'recommended_practice': self.recommend_practice(soul_id).name if self.recommend_practice(soul_id) else None,
            'average_aspect_integration': avg_integration_level
        }
    
    def save_shadow_data(self):
        """Save all shadow data to files"""
        shadow_data_dir = Path(__file__).parent.parent.parent / 'data' / 'shadow_work'
        shadow_data_dir.mkdir(exist_ok=True)
        
        # Save shadow aspects
        aspects_data = {}
        for aspect_id, aspect in self.shadow_aspects.items():
            aspects_data[aspect_id] = {
                'name': aspect.name,
                'archetype': aspect.archetype.value,
                'description': aspect.description,
                'triggers': aspect.triggers,
                'gifts': aspect.gifts,
                'challenges': aspect.challenges,
                'integration_level': aspect.integration_level,
                'last_encountered': aspect.last_encountered
            }
        
        with open(shadow_data_dir / 'shadow_aspects.json', 'w') as f:
            json.dump(aspects_data, f, indent=2)
        
        # Save dialogue history
        dialogue_data = [
            {
                'dialogue_id': d.dialogue_id,
                'soul_id': d.soul_id,
                'aspect_id': d.aspect_id,
                'question': d.question,
                'shadow_response': d.shadow_response,
                'persona_response': d.persona_response,
                'integration_insight': d.integration_insight,
                'timestamp': d.timestamp,
                'emotional_state': d.emotional_state,
                'sovereignty_check': d.sovereignty_check
            }
            for d in self.dialogue_history
        ]
        
        with open(shadow_data_dir / 'dialogue_history.json', 'w') as f:
            json.dump(dialogue_data, f, indent=2)
        
        # Save integration tracking
        integration_data = {}
        for soul_id, integration in self.integration_tracking.items():
            integration_data[soul_id] = {
                'soul_id': integration.soul_id,
                'integration_score': integration.integration_score,
                'dominant_aspects': integration.dominant_aspects,
                'dormant_aspects': integration.dormant_aspects,
                'sovereignty_level': integration.sovereignty_level,
                'last_practice_date': integration.last_practice_date,
                'practice_streak': integration.practice_streak,
                'integration_milestones': integration.integration_milestones
            }
        
        with open(shadow_data_dir / 'integration_tracking.json', 'w') as f:
            json.dump(integration_data, f, indent=2)
        
        self.logger.info("Shadow data saved successfully")
