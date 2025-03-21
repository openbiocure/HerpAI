import yaml
from dataclasses import dataclass, field

@dataclass
class AgentConfig:
    model_provider: str
    model: str
    prompt_version: str = "v1"
    cache: bool = False
    max_tokens: int = 1000
    temperature: float = 0.5

@dataclass
class AppConfig:
    default_model_provider: str
    agents: dict = field(default_factory=dict)

    @classmethod
    def load(cls, path="config.yaml"):
        with open(path, "r") as f:
            raw_cfg = yaml.safe_load(f)

        agents_cfg = {
            name: AgentConfig(
                model_provider=agent.get("model_provider", raw_cfg["default_model_provider"]),
                model=agent["model"],
                prompt_version=agent.get("prompt_version", "v1"),
                cache=agent.get("cache", False),
                max_tokens=agent.get("max_tokens", 1000),
                temperature=agent.get("temperature", 0.5)
            )
            for name, agent in raw_cfg.get("agents", {}).items()
        }

        return cls(
            default_model_provider=raw_cfg["default_model_provider"],
            agents=agents_cfg
        )

    def get_agent(self, agent_name: str) -> AgentConfig:
        return self.agents.get(agent_name, AgentConfig(
            model_provider=self.default_model_provider, model="default-model"))
