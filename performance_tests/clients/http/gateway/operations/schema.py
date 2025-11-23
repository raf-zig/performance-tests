from pydantic import BaseModel, Field, ConfigDict
from enum import StrEnum
from performance_tests.tools.fakers import fake

class OperationType(StrEnum):
    """
        Описание структуры типов операций.
    """
    FEE = "FEE"
    TOP_UP = "TOP_UP"
    TRANSFER = "TRANSFER"

class OperationStatus(StrEnum):
    """
        Описание структуры статуса.
    """
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"
    IN_PROGRESS = "IN_PROGRESS"
    UNSPECIFIED = "UNSPECIFIED"

class OperationSchema(BaseModel):
    """
        Описание структуры операций.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str
    type: OperationType
    status: OperationStatus
    amount: int
    card_id: str = Field(alias="cardId")
    category: str
    created_at: str = Field(alias="createdAt")
    account_id: str = Field(alias="accountId")

class OperationReceiptSchema(BaseModel):
    """
        Описание структуры Receipt.
    """
    url: str
    document: str

class OperationsSummarySchema(BaseModel):
    """
            Описание структуры Summary.
    """
    spent_amount: int = Field(alias="spentAmount")
    received_amount: int = Field(alias="receivedAmount")
    cashback_amount: int = Field(alias="cashbackAmount")

class GetOperationsQuerySchema(BaseModel):
    """
                Описание структуры OperationsQuery.
    """
    account_id: str = Field(alias="accountId")

class GetOperationsResponseSchema(BaseModel):
    operations: list[OperationSchema]

class GetOperationReceiptResponseSchema(BaseModel):
    receipt: OperationReceiptSchema

class GetOperationSummaryResponseSchema(BaseModel):
    summary: OperationsSummarySchema

class GetOperationsSummaryQuerySchema(BaseModel):
    """
                    Описание структуры OperationsSummary.
    """
    account_id: str = Field(alias="accountId")

class MakeOperationRequestSchema(BaseModel):
    """
                        Описание структуры MakeOperationRequest.
    """
    model_config = ConfigDict(populate_by_name=True)

    status: OperationStatus = Field(default_factory=lambda: fake.enum(OperationStatus))
    amount: int = Field(default_factory=lambda: fake.amount())
    card_id: str = Field(alias="cardId")
    account_id: str = Field(alias="accountId")


class MakeOperationResponseSchema(BaseModel):
    operation: OperationSchema

class MakeFeeOperationRequestSchema(MakeOperationRequestSchema):
    pass

class MakeFeeOperationResponseSchema(MakeOperationResponseSchema):
    pass

class MakeTopUpOperationRequestSchema(MakeOperationRequestSchema):
    pass

class MakeTopUpOperationResponseSchema(MakeOperationResponseSchema):
    pass

class MakeCashbackOperationRequestSchema(MakeOperationRequestSchema):
    pass

class MakeCashbackOperationResponseSchema(MakeOperationResponseSchema):
    pass

class MakeTransferOperationRequestSchema(MakeOperationRequestSchema):
    pass

class MakeTransferOperationResponseSchema(MakeOperationResponseSchema):
    pass

class MakeBillPaymentOperationRequestSchema(MakeOperationRequestSchema):
    pass

class MakeBillPaymentOperationResponseSchema(MakeOperationResponseSchema):
    pass

class MakeCashWithdrawalOperationRequestSchema(MakeOperationRequestSchema):
    pass

class MakeCashWithdrawalOperationResponseSchema(MakeOperationResponseSchema):
    pass

class MakePurchaseOperationRequestSchema(MakeOperationRequestSchema):
    category: str = Field(default_factory=lambda: fake.category())

class MakePurchaseOperationResponseSchema(MakeOperationResponseSchema):
    pass