from pydantic import BaseModel, HttpUrl

class DocumentSchema(BaseModel):
    url: HttpUrl
    document: str

class GetTariffDocumentResponseSchema(BaseModel):
    """
    Структура данных для получения тарифa по счету.
    """
    tariff: DocumentSchema


class GetContractDocumentResponseSchema(BaseModel):
    """
    Структура данных для получения контракта по счету.
    """
    contract: DocumentSchema
