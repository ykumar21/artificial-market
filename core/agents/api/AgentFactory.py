import configparser

from core.agents.api.types import RandomAgent, PassiveAgent

class AgentFactory:
    @staticmethod
    def create_agent(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)

        agent_type = config.get('Agent', 'type')

        if agent_type == 'RandomAgent':
            return RandomAgent(config_file)
        elif agent_type == 'PassiveAgent':
            return PassiveAgent(config_file)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
