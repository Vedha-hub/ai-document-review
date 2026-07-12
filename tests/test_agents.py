import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.writer_agent import run_writer_agent
from agents.critic_agent import run_critic_agent

def test_writer_returns_string():
    result = run_writer_agent('Build a todo app')
    assert isinstance(result, str)
    assert len(result) > 100
    print("✅ Writer returns string — PASSED")

def test_critic_returns_dict():
    result = run_critic_agent('Simple PRD about todo app.')
    assert isinstance(result, dict)
    assert 'status' in result
    assert 'score' in result
    print("✅ Critic returns dict — PASSED")

if __name__ == '__main__':
    test_writer_returns_string()
    test_critic_returns_dict()
    print("\n✅ All tests passed!")