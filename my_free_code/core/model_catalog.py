from .gateway_models import GatewayModel

def build_gateway_models(config):
    return [
        GatewayModel("claude-opus", "opus", True),
        GatewayModel("claude-opus-no-thinking", "opus", False),
        GatewayModel("claude-sonnet", "sonnet", True),
        GatewayModel("claude-sonnet-no-thinking", "sonnet", False),
        GatewayModel("claude-haiku", "haiku", True),
        GatewayModel("claude-haiku-no-thinking", "haiku", False),
        GatewayModel("claude-fable", "fable", True),
    ]

def public_catalog(config):
    direct = [x for x in {
        config.model, config.fable, config.opus, config.sonnet, config.haiku,
        *config.fallbacks
    } if x and "/" in x]
    gateways = [x.id for x in build_gateway_models(config)]
    return list(dict.fromkeys(gateways + direct))
