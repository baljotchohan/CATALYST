from anthropic import Anthropic
from datetime import datetime
import json
from backend.models.agent_decision import AgentDecision
from backend.data_sources.api_manager import APIManager
from backend.core.simulation_engine import SimulationEngine
from backend.models.agent import Agent

class UnifiedAgent(Agent):
    """Base class for all agents"""

    def __init__(self, name: str, simulation_engine: SimulationEngine):
        super().__init__(name, simulation_engine)
        self.client = Anthropic()

    async def analyze_with_claude(self, prompt, max_tokens=1000) -> AgentDecision:
        """Call Claude API for analysis and get a structured decision."""
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            structured_response = response.content[0].text
            
            # Find the JSON part of the response
            json_start = structured_response.find('''{''')
            json_end = structured_response.rfind('''}''') + 1
            json_str = structured_response[json_start:json_end]
            
            data = json.loads(json_str)
            return AgentDecision(**data)
        except Exception as e:
            print(f"Claude API error: {e}")
            # Fallback decision
            return AgentDecision(
                analysis="Analysis unavailable - using fallback models.",
                recommendation="Default recommendation.",
                impact={}
            )

    def run(self) -> AgentDecision:
        raise NotImplementedError

class WeatherAgent(UnifiedAgent):
    def __init__(self, simulation_engine: SimulationEngine):
        super().__init__("Weather Advisor", simulation_engine)

    async def run(self) -> AgentDecision:
        weather_data = await APIManager.fetch_weather()
        prices_data = await APIManager.fetch_commodity_prices()

        prompt = f'''
        You are an agricultural weather expert. Analyze this data:

        WEATHER DATA: {weather_data}
        COMMODITY PRICES: {prices_data}

        Provide your response as a JSON object with the following keys: "analysis", "recommendation", and "impact".
        The "impact" should be a dictionary with keys "gdp", "stability", and "resources".

        Example response:
        '''
        {
            "analysis": "Drought conditions are severe in the northern regions, which will negatively affect crop yields.",
            "recommendation": "Implement immediate water rationing and deploy emergency irrigation resources to the northern regions.",
            "impact": {
                "gdp": -50,
                "stability": -5,
                "resources": -10
            }
        }
        '''
        '''

        decision = await self.analyze_with_claude(prompt)
        self.apply_impact(decision)
        return decision

class HealthAgent(UnifiedAgent):
    def __init__(self, simulation_engine: SimulationEngine):
        super().__init__("Health Tracker", simulation_engine)

    async def run(self) -> AgentDecision:
        health_data = await APIManager.fetch_health_data()

        prompt = f'''
        You are a disease epidemiologist. Analyze this health data:

        HEALTH DATA: {health_data}

        Provide your response as a JSON object with the following keys: "analysis", "recommendation", and "impact".
        The "impact" should be a dictionary with keys "gdp", "stability", and "resources".
        '''

        decision = await self.analyze_with_claude(prompt)
        self.apply_impact(decision)
        return decision

class FarmAgent(UnifiedAgent):
    def __init__(self, simulation_engine: SimulationEngine):
        super().__init__("Farm Advisor", simulation_engine)

    async def run(self) -> AgentDecision:
        weather_data = await APIManager.fetch_weather()
        prices_data = await APIManager.fetch_commodity_prices()

        prompt = f'''
        You are an expert agricultural advisor. Analyze this data:

        WEATHER: {weather_data}
        PRICES: {prices_data}

        Provide your response as a JSON object with the following keys: "analysis", "recommendation", and "impact".
        The "impact" should be a dictionary with keys "gdp", "stability", and "resources".
        '''

        decision = await self.analyze_with_claude(prompt)
        self.apply_impact(decision)
        return decision

class SecurityAgent(UnifiedAgent):
    def __init__(self, simulation_engine: SimulationEngine):
        super().__init__("Security Analyst", simulation_engine)

    async def run(self) -> AgentDecision:
        crime_data = await APIManager.fetch_crime_data()

        prompt = f'''
        You are a crime analyst. Analyze this data:

        CRIME DATA: {crime_data}

        Provide your response as a JSON object with the following keys: "analysis", "recommendation", and "impact".
        The "impact" should be a dictionary with keys "gdp", "stability", and "resources".
        '''

        decision = await self.analyze_with_claude(prompt)
        self.apply_impact(decision)
        return decision

class EducationAgent(UnifiedAgent):
    def __init__(self, simulation_engine: SimulationEngine):
        super().__init__("Education Analyst", simulation_engine)

    async def run(self) -> AgentDecision:
        edu_data = await APIManager.fetch_education_data()

        prompt = f'''
        You are an education policy expert. Analyze this data:

        EDUCATION DATA: {edu_data}

        Provide your response as a JSON object with the following keys: "analysis", "recommendation", and "impact".
        The "impact" should be a dictionary with keys "gdp", "stability", and "resources".
        '''

        decision = await self.analyze_with_claude(prompt)
        self.apply_impact(decision)
        return decision