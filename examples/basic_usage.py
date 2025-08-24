#!/usr/bin/env python3
"""
Basic usage example for the Proof-of-Intent SDK.

This example demonstrates:
1. Creating a PoI receipt
2. Signing the receipt
3. Validating the receipt
4. Basic receipt operations
"""

from poi_sdk import PoIGenerator, PoIValidator, PoIReceipt


def main():
    """Main example function."""
    print("🔐 Proof-of-Intent SDK - Basic Usage Example")
    print("=" * 50)
    
    # Initialize the generator and validator
    print("\n1. Initializing PoI components...")
    generator = PoIGenerator()
    validator = PoIValidator()
    
    print(f"   Generator: {generator}")
    print(f"   Validator: {validator}")
    
    # Generate a receipt
    print("\n2. Generating a PoI receipt...")
    receipt = generator.generate_receipt(
        agent_id="example_agent_001",
        action="database_query",
        target_resource="user_profiles",
        declared_objective="Read user profile for authentication",
        risk_context="low",
        additional_context={
            "session_id": "sess_12345",
            "user_ip": "192.168.1.100",
            "request_type": "login"
        }
    )
    
    print(f"   Receipt generated: {receipt.receipt_id}")
    print(f"   Agent: {receipt.agent_id}")
    print(f"   Action: {receipt.action}")
    print(f"   Resource: {receipt.target_resource}")
    print(f"   Objective: {receipt.declared_objective}")
    print(f"   Risk: {receipt.risk_context}")
    print(f"   Expires: {receipt.expiration_time}")
    
    # Validate the receipt
    print("\n3. Validating the receipt...")
    try:
        is_valid = validator.validate_receipt(receipt)
        if is_valid:
            print("Receipt is valid!")
        else:
            print("Receipt validation failed!")
    except Exception as e:
        print(f"Validation error: {e}")
    
    # Check receipt status
    print("\n4. Checking receipt status...")
    if receipt.is_expired():
        print("Receipt has expired")
    else:
        time_left = receipt.time_until_expiration()
        if time_left:
            print(f"Receipt is valid (expires in {time_left:.0f} seconds)")
        else:
            print("Receipt is valid")
    
    # Add audit entry
    print("\n5. Adding audit entry...")
    receipt.add_audit_entry(
        action="receipt_accessed",
        details={
            "access_time": "2024-01-15T10:30:00Z",
            "access_method": "api_call",
            "user_agent": "example_client/1.0"
        }
    )
    print(f"   Audit trail entries: {len(receipt.audit_trail)}")
    
    # Add compliance tag
    print("\n6. Adding compliance tag...")
    receipt.add_compliance_tag("GDPR")
    receipt.add_compliance_tag("SOC2")
    print(f"   Compliance tags: {receipt.compliance_tags}")
    
    # Convert to different formats
    print("\n7. Converting receipt formats...")
    receipt_dict = receipt.to_dict()
    receipt_json = receipt.to_json(indent=2)
    
    print(f"Dictionary keys: {list(receipt_dict.keys())}")
    print(f"JSON length: {len(receipt_json)} characters")
    
    # Show signature information
    print("\n8. Signature information...")
    if receipt.signature:
        print(f"Algorithm: {receipt.signature_algorithm}")
        print(f"Signature: {receipt.signature[:50]}...")
        print(f"Signature length: {len(receipt.signature)} characters")
    else:
        print("No signature available")
    
    # Show additional context
    print("\n9. Additional context...")
    if receipt.additional_context:
        for key, value in receipt.additional_context.items():
            print(f"   {key}: {value}")
    else:
        print("   No additional context")
    
    print("\n" + "=" * 50)
    print("Basic usage example completed successfully!")
    print(f"Receipt ID: {receipt.receipt_id}")
    print("Check the generated receipt above for all details")


if __name__ == "__main__":
    main()
