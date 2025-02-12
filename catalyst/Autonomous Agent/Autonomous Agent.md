# Autonomous Agent
最早出现的 Autonomous Agent 开发框架是 AutoGPT，最初名叫 EntreprenurGPT，由英国游戏开发者 Toran Bruce Richards 开发，于 2023 年 3 月 16 日在 GitHub 上发布。

AutoGPT 结合了 GPT-4 和 GPT-3.5 模型，通过 API 来创建完整的项目。它可以根据用户给定的目标，自动生成所需的提示词，并执行多步骤任务，不需要人类的干预和指导。AutoGPT 弥补了 GPT-4 的缺点，实现了任务执行的自动化，这也是 AutoGPT 能在短时间内爆火的原因。AutoGPT 相当于给了 GPT-4 一个“身体”，充当了它的“四肢”，从而对大语言模型生成的内容实现了更深层次的应用。

随后在很短时间内，开源社区涌现出大量类似 AutoGPT 这样的 Autonomous Agent 开发框架，例如 Camel、BabyAGI、MetaGPT、AutoGen（微软）、AutoAgents、AgentGPT、Swarm（OpenAI）等等。随着这些开发框架的发展壮大，它们都已经能够支持开发复杂的多 Agent 应用，多 Agent 应用通常都是基于角色扮演（role playing）来实现的，即每个 Agent 扮演一个角色（或岗位），仅完成这个角色（或岗位）需要完成的工作，通过事先定义的工作流相互协作。

Autonomous Agent 开发框架最好是轻量级的，不要过度封装。我们不需要重量级开发框架，特别不需要那种要么全有、要么全无的开发框架。过犹不及，一旦过度封装，当基础 LLM 的新版本提供了一些全新功能时，通过重量级开发框架往往难以及时利用这些新功能。

除了 Autonomous Agent 开发框架外，我们还很有必要学习一类自动提示词工程开发框架。这类开发框架可以缓解并解决复杂手工提示词工程中存在的工作繁重、脆弱、不可移植、技能难以在团队中传播等等严重问题。我将选择此类开发框架中诞生最早的 DSPy 来做讲解。DSPy 也可以被集成在 Autonomous Agent 开发框架之中。