from ..models.fintech_models import ProductType, QueryIntent

INTENT_MAP = {
    # General & Fallback
    "pregunta_fuera_de_contexto": QueryIntent.GENERAL,
    "finalizar_conversacion": QueryIntent.GENERAL,
    "consulta_general": QueryIntent.GENERAL,
    "consulta_externa": QueryIntent.GENERAL,
    "informacion_general": QueryIntent.GENERAL,
    "otro": QueryIntent.OTRO,
    "no_aplica": QueryIntent.OTRO,
    # Benefits
    "consultar_beneficios": QueryIntent.BENEFITS,
    "beneficios": QueryIntent.BENEFITS,
    # Requirements
    "consultar_requisitos": QueryIntent.REQUIREMENTS,
    "requisitos": QueryIntent.REQUIREMENTS,
    # Fees & Rates
    "consultar_tasa_interes": QueryIntent.FEES_RATES,
    "consultar_tasas": QueryIntent.FEES_RATES,
    "tasas": QueryIntent.FEES_RATES,
    # Application Process
    "solicitar_producto": QueryIntent.APPLICATION_PROCESS,
    "proceso_de_solicitud": QueryIntent.APPLICATION_PROCESS,
    "solicitud_de_producto": QueryIntent.APPLICATION_PROCESS,
    # Comparison
    "consultar_diferencias": QueryIntent.GENERAL,
    "comparar_productos": QueryIntent.GENERAL,
    "comparacion_de_productos": QueryIntent.GENERAL,
}

PRODUCT_MAP = {
    # Debit Card
    "tarjeta_de_debito": ProductType.DEBIT_CARD,
    "tarjeta_debito": ProductType.DEBIT_CARD,
    # Loan
    "prestamo_personal": ProductType.LOAN,
    "prestamo": ProductType.LOAN,
    # Credit Card
    "tarjeta_de_credito": ProductType.CREDIT_CARD,
    "tarjeta_credito": ProductType.CREDIT_CARD,
    # No aplica / Comparison
    "tarjeta_de_debito/tarjeta_de_credito": ProductType.NO_APLICA,
    "tarjeta_de_debito_vs_tarjeta_de_credito": ProductType.NO_APLICA,
    "otro": ProductType.NO_APLICA,
    "no_aplica": ProductType.NO_APLICA,
}
