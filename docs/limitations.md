# Limitations

- The initial mutation engine uses explicit operators rather than parsing arbitrary languages.
- The demo uses a small synthetic application.
- A surviving mutant is not automatically a real defect; equivalent behavior can exist.
- The deterministic AI fallback is not an LLM and is included for reproducibility.
- LLM integrations should validate outputs and isolate generated code before execution.
