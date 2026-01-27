"""
LLM Service for Ollama API interactions.
Handles all communication with the Ollama API.
"""
import requests
import logging
from typing import Optional

from backend.config import get_settings

logger = logging.getLogger(__name__)


# Prompt templates for different review types
REVIEW_PROMPTS = {
    "general": """You are a senior developer performing a comprehensive code review.
Review the following code for:
- Bugs and potential issues
- Code quality and best practices
- Performance improvements
- Readability and maintainability

Be specific with line numbers when pointing out issues. Format your response clearly.

Code to review:
```{language}
{code}
```""",
    
    "bugs": """You are a bug detection expert. Analyze the following code ONLY for bugs and errors.
Focus on:
- Logic errors
- Off-by-one errors
- Null/undefined handling
- Edge cases
- Runtime exceptions

List each bug with its location and suggested fix.

Code to analyze:
```{language}
{code}
```""",
    
    "quality": """You are a code quality expert. Review the following code for best practices.
Focus on:
- Naming conventions
- Code organization
- DRY principle violations
- SOLID principles
- Documentation/comments

Provide specific suggestions for improvement.

Code to review:
```{language}
{code}
```""",
    
    "performance": """You are a performance optimization expert. Analyze the following code for efficiency.
Focus on:
- Time complexity
- Space complexity
- Inefficient operations
- Memory leaks
- Caching opportunities

Provide specific optimization suggestions.

Code to analyze:
```{language}
{code}
```""",
    
    "security": """You are a security expert. Analyze the following code for vulnerabilities.
Focus on:
- Injection vulnerabilities
- Authentication/authorization issues
- Data exposure risks
- Input validation
- Secure coding practices

List each vulnerability with severity and remediation steps.

Code to analyze:
```{language}
{code}
```"""
}


class LLMService:
    """Service for interacting with Ollama LLM."""
    
    def __init__(self):
        self.settings = get_settings()
    
    def check_connection(self) -> bool:
        """Check if Ollama is reachable."""
        try:
            # Try to reach Ollama API
            response = requests.get(
                self.settings.ollama_url.replace("/api/generate", "/api/tags"),
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama connection check failed: {e}")
            return False
    
    def get_review(
        self, 
        code: str, 
        review_type: str = "general",
        language: Optional[str] = None
    ) -> str:
        """
        Get code review from Ollama.
        
        Args:
            code: The code to review
            review_type: Type of review (general, bugs, quality, performance, security)
            language: Programming language (optional)
            
        Returns:
            Review text from the LLM
            
        Raises:
            ConnectionError: If Ollama is not reachable
            TimeoutError: If request times out
            Exception: For other errors
        """
        # Get the appropriate prompt template
        prompt_template = REVIEW_PROMPTS.get(review_type, REVIEW_PROMPTS["general"])
        
        # Detect language if not provided
        if not language:
            language = self._detect_language(code)
        
        # Format the prompt
        prompt = prompt_template.format(code=code, language=language)
        
        try:
            logger.info(f"Sending {review_type} review request to Ollama")
            
            response = requests.post(
                self.settings.ollama_url,
                json={
                    "model": self.settings.model_name,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=self.settings.request_timeout
            )
            
            if response.status_code != 200:
                raise Exception(f"Ollama returned status {response.status_code}")
            
            result = response.json()
            return result.get("response", "").strip()
            
        except requests.exceptions.Timeout:
            logger.error("Ollama request timed out")
            raise TimeoutError("Request timed out. The code might be too long or complex.")
        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to Ollama")
            raise ConnectionError("Cannot connect to Ollama. Is it running?")
        except Exception as e:
            logger.error(f"LLM request failed: {e}")
            raise
    
    def _detect_language(self, code: str) -> str:
        """Simple language detection based on code patterns."""
        code_lower = code.lower()
        
        # Check for common patterns
        if "def " in code and ":" in code:
            return "python"
        elif "function " in code or "const " in code or "let " in code:
            return "javascript"
        elif "public class " in code or "private " in code:
            return "java"
        elif "#include" in code:
            return "cpp"
        elif "func " in code and "{" in code:
            return "go"
        elif "<html" in code_lower or "<!doctype" in code_lower:
            return "html"
        elif "select " in code_lower and "from " in code_lower:
            return "sql"
        else:
            return "code"


# Singleton instance
llm_service = LLMService()
