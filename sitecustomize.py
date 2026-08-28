"""
Automatic Hugging Face Mirror Patch for Kimodo AI Virtual Stage.
Redirects gated Meta-Llama-3-8B-Instruct requests to the open, ungated
NousResearch/Meta-Llama-3-8B-Instruct repository to bypass 403 Forbidden gating errors.
"""
import sys

try:
    import huggingface_hub

    _orig_hf_hub_download = huggingface_hub.hf_hub_download
    _orig_snapshot_download = huggingface_hub.snapshot_download

    def _patched_hf_hub_download(*args, **kwargs):
        if kwargs.get("repo_id") == "meta-llama/Meta-Llama-3-8B-Instruct":
            kwargs["repo_id"] = "NousResearch/Meta-Llama-3-8B-Instruct"
        elif len(args) > 0 and args[0] == "meta-llama/Meta-Llama-3-8B-Instruct":
            args = ("NousResearch/Meta-Llama-3-8B-Instruct",) + args[1:]
        return _orig_hf_hub_download(*args, **kwargs)

    def _patched_snapshot_download(*args, **kwargs):
        if kwargs.get("repo_id") == "meta-llama/Meta-Llama-3-8B-Instruct":
            kwargs["repo_id"] = "NousResearch/Meta-Llama-3-8B-Instruct"
        elif len(args) > 0 and args[0] == "meta-llama/Meta-Llama-3-8B-Instruct":
            args = ("NousResearch/Meta-Llama-3-8B-Instruct",) + args[1:]
        return _orig_snapshot_download(*args, **kwargs)

    huggingface_hub.hf_hub_download = _patched_hf_hub_download
    huggingface_hub.snapshot_download = _patched_snapshot_download

except ImportError:
    pass
