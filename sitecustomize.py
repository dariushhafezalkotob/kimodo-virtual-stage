"""
Automatic Hugging Face Mirror Patch for Kimodo AI Virtual Stage.
Redirects gated Meta-Llama-3-8B-Instruct requests to the open, ungated
NousResearch/Meta-Llama-3-8B-Instruct repository to bypass 403 Forbidden gating errors.
"""
import sys
import os

def _rewrite(repo_id):
    if isinstance(repo_id, str) and repo_id == "meta-llama/Meta-Llama-3-8B-Instruct":
        return "NousResearch/Meta-Llama-3-8B-Instruct"
    return repo_id

# 1. Patch huggingface_hub
try:
    import huggingface_hub
    import huggingface_hub.file_download

    _orig_hf_download = huggingface_hub.hf_hub_download
    _orig_file_download = huggingface_hub.file_download.hf_hub_download
    _orig_snapshot_download = huggingface_hub.snapshot_download

    def _patched_hf_download(*args, **kwargs):
        if "repo_id" in kwargs:
            kwargs["repo_id"] = _rewrite(kwargs["repo_id"])
        elif len(args) > 0:
            args = (_rewrite(args[0]),) + args[1:]
        return _orig_hf_download(*args, **kwargs)

    def _patched_file_download(*args, **kwargs):
        if "repo_id" in kwargs:
            kwargs["repo_id"] = _rewrite(kwargs["repo_id"])
        elif len(args) > 0:
            args = (_rewrite(args[0]),) + args[1:]
        return _orig_file_download(*args, **kwargs)

    def _patched_snapshot_download(*args, **kwargs):
        if "repo_id" in kwargs:
            kwargs["repo_id"] = _rewrite(kwargs["repo_id"])
        elif len(args) > 0:
            args = (_rewrite(args[0]),) + args[1:]
        return _orig_snapshot_download(*args, **kwargs)

    huggingface_hub.hf_hub_download = _patched_hf_download
    huggingface_hub.file_download.hf_hub_download = _patched_file_download
    huggingface_hub.snapshot_download = _patched_snapshot_download
except Exception as e:
    pass

# 2. Patch transformers
try:
    import transformers
    import transformers.utils.hub
    import transformers.configuration_utils

    if hasattr(transformers.utils.hub, "cached_file"):
        _orig_cached_file = transformers.utils.hub.cached_file
        def _patched_cached_file(path_or_repo_id, *args, **kwargs):
            return _orig_cached_file(_rewrite(path_or_repo_id), *args, **kwargs)
        transformers.utils.hub.cached_file = _patched_cached_file

    if hasattr(transformers.utils.hub, "cached_files"):
        _orig_cached_files = transformers.utils.hub.cached_files
        def _patched_cached_files(path_or_repo_id, *args, **kwargs):
            return _orig_cached_files(_rewrite(path_or_repo_id), *args, **kwargs)
        transformers.utils.hub.cached_files = _patched_cached_files

    if hasattr(transformers.configuration_utils.PretrainedConfig, "get_config_dict"):
        _orig_config_get_dict = transformers.configuration_utils.PretrainedConfig.get_config_dict
        def _patched_config_get_dict(pretrained_model_name_or_path, *args, **kwargs):
            return _orig_config_get_dict(_rewrite(pretrained_model_name_or_path), *args, **kwargs)
        transformers.configuration_utils.PretrainedConfig.get_config_dict = _patched_config_get_dict

except Exception as e:
    pass
