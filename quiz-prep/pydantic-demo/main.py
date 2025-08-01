from datetime import datetime
from typing import Annotated, Optional, Dict
from pydantic import BaseModel, Field, ValidationError, field_validator, TypeAdapter
import time

# Pydantic V2 uses Annotated and Field for constraints, replacing Constrained* types [5, 6].
# PositiveInt is an example of such a type (equivalent to Annotated[int, annotated_types.Gt(0)]) [6].
# For demonstration, I'll explicitly use Annotated and Field for a similar effect.

class User(BaseModel):
    """A Pydantic model demonstrating basic data validation."""
    id: int
    name: str = "jamila"
    # In V2, Optional[str] without a default is a required field that can be None [8, 9].
    signup_ts: Optional[datetime]
    # Tastes is a dictionary where keys are strings and values are integers greater than 0.
    # We use Annotated and Field to apply the 'greater than 0' constraint [6, 10].
    tastes: Dict[str, Annotated[int, Field(gt=0)]]
    # You could also define a custom field validator (new @field_validator in V2) [11, 12]
    # For instance, to ensure 'name' is always capitalized:
    @field_validator('name', mode='before')
    @classmethod
    def capitalize_name(cls, v: str) -> str:
        return v.capitalize()
    model_config = {"validate_default": True}


def main():
    """Demonstrate basic Pydantic usage and validation."""
    print("--- Pydantic Demonstration ---")
    # 1. Successful Validation
    print("\nAttempting successful validation:")
    external_data = {
        'id': 123,
        'signup_ts': '2023-01-15T10:30:00Z',  # Pydantic coerces string to datetime [6, 13]
        'tastes': {
            'coffee': 8,
            'chocolate': 10,
            'tea': '5' # Pydantic coerces string '5' to int 5 [6, 14]
        },
    }
    try:
        user_instance = User(**external_data)  # Instantiate the model [7]
        print(f"Validation successful!")
        time.sleep(1)  # Simulate some processing time
        print(f"User ID: {user_instance.id}")  # Access fields as attributes [7]
        time.sleep(1)
        print(f"User Name: {user_instance.name}")
        time.sleep(1)
        print(f"Signup Timestamp: {user_instance.signup_ts}")
        time.sleep(1)
        print(f"User Tastes: {user_instance.tastes}")
        time.sleep(1)

        # Convert the model to a Python dictionary (model_dump() replaces dict() in V2) [7, 15, 16]
        print(f"Model as dictionary: {user_instance.model_dump()}")
        time.sleep(1)

        # Convert the model to JSON string (model_dump_json() replaces json() in V2) [15, 17]
        print(f"Model as JSON: {user_instance.model_dump_json(indent=2)}")

    except ValidationError as e:
        print(f"Validation Error occurred: {e}")
    
    # 2. Failed Validation and Error Handling [18]
    print("\nAttempting failed validation:")
    external_data_invalid = {
        'id': 'not-an-int',  # Invalid type for 'id' [18]
        'tastes': {
            'salty': -1,  # Value violates 'gt=0' constraint
            'sweet': 5
        },
        # 'signup_ts' is missing and is a required field (even if Optional[datetime]) [8, 18]
    }

    try:
        User(**external_data_invalid)
    except ValidationError as e:
        
        print(f"Validation failed as expected. Error details:")
        # Print a list of validation errors [18]
        for error in e.errors():
            print(f"  - Type: {error['type']}, Location: {error['loc']}, Message: {error['msg']}")
            # In V2, TypeError is no longer automatically converted to ValidationError [19, 20].
    
    # 3. Brief mention of TypeAdapter for non-BaseModel types [21, 22]
    time.sleep(1)
    print("\n--- TypeAdapter Example ---")
    print("Pydantic V2 introduced TypeAdapter for validating and serialising non-BaseModel types [21, 22].")
    print("It replaces 'parse_obj_as' and 'schema_of' utility functions [21].")
    
    # Example: Validating a list of integers
    list_adapter = TypeAdapter(list[int])
    try:
        validated_list = list_adapter.validate_python(['1', '2', 3.0])
        time.sleep(1)
        print(f"Validated list using TypeAdapter: {validated_list}")
        time.sleep(1)
        print(f"JSON Schema for list[int]: {list_adapter.json_schema()}")
    except ValidationError as e:
        print(f"TypeAdapter validation error: {e}")


if __name__ == "__main__":
    main()
