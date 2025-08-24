#!/usr/bin/env python3
"""
Simple PoI SDK Demo Script

This script demonstrates the core functionality of the Proof-of-Intent SDK.
"""

from poi_sdk import PoIGenerator, PoIValidator, PoIReceipt


def main():
    """Main demo function."""
    print("🔐 PoI SDK Demo - Building Trustworthy AI Agents")
    print("=" * 60)
    
    # Initialize components
    print("\n1. 🚀 Initializing PoI SDK...")
    generator = PoIGenerator()
    validator = PoIValidator()
    
    print(f"   ✅ Generator ready: {generator}")
    print(f"   ✅ Validator ready: {validator}")
    
    # Generate receipts for different scenarios
    scenarios = [
        {
            "name": "Database Access",
            "agent_id": "data_agent_001",
            "action": "database_query",
            "resource": "customer_database",
            "objective": "Fetch customer information for billing",
            "risk": "medium"
        },
        {
            "name": "API Call",
            "agent_id": "api_agent_001", 
            "action": "http_request",
            "resource": "https://api.payment.com/transactions",
            "objective": "Process payment transaction",
            "risk": "high"
        },
        {
            "name": "File Operation",
            "agent_id": "file_agent_001",
            "action": "file_read",
            "resource": "/var/log/system.log",
            "objective": "Analyze system performance",
            "risk": "low"
        }
    ]
    
    receipts = []
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. 📋 Generating receipt for: {scenario['name']}")
        
        receipt = generator.generate_receipt(
            agent_id=scenario["agent_id"],
            action=scenario["action"],
            target_resource=scenario["resource"],
            declared_objective=scenario["objective"],
            risk_context=scenario["risk"],
            additional_context={
                "scenario": scenario["name"],
                "priority": "normal",
                "request_id": f"req_{i:03d}"
            }
        )
        
        print(f"   🆔 Receipt ID: {receipt.receipt_id}")
        print(f"   🤖 Agent: {receipt.agent_id}")
        print(f"   ⚡ Action: {receipt.action}")
        print(f"   🎯 Objective: {receipt.declared_objective}")
        print(f"   ⚠️  Risk: {receipt.risk_context}")
        print(f"   ⏰ Expires: {receipt.expiration_time}")
        
        receipts.append(receipt)
    
    # Validate receipts
    print(f"\n4. 🔍 Validating {len(receipts)} receipts...")
    
    for i, receipt in enumerate(receipts, 1):
        try:
            is_valid = validator.validate_receipt(receipt)
            status = "✅ Valid" if is_valid else "❌ Invalid"
            print(f"   Receipt {i}: {status}")
        except Exception as e:
            print(f"   Receipt {i}: ❌ Error - {e}")
    
    # Show receipt details
    print(f"\n5. 📊 Receipt Details Summary")
    print(f"   Total receipts: {len(receipts)}")
    
    for i, receipt in enumerate(receipts, 1):
        print(f"\n   Receipt {i}: {receipt.receipt_id}")
        print(f"     Agent: {receipt.agent_id}")
        print(f"     Action: {receipt.action}")
        print(f"     Resource: {receipt.target_resource}")
        print(f"     Risk: {receipt.risk_context}")
        print(f"     Expires in: {receipt.time_until_expiration():.0f} seconds")
        
        if receipt.signature:
            print(f"     Signature: {receipt.signature[:30]}...")
            print(f"     Algorithm: {receipt.signature_algorithm}")
    
    # Demonstrate batch operations
    print(f"\n6. 🔄 Batch Operations Demo")
    
    # Batch validation
    validation_results = validator.validate_receipt_batch(receipts)
    valid_count = sum(validation_results.values())
    print(f"   Batch validation: {valid_count}/{len(receipts)} receipts valid")
    
    # Get validation summary
    summary = validator.get_validation_summary(receipts)
    print(f"   Validation rate: {summary['validation_rate']:.1%}")
    
    # Show what we've accomplished
    print(f"\n" + "=" * 60)
    print("🎉 Demo Completed Successfully!")
    print("=" * 60)
    print("✅ Generated cryptographically signed PoI receipts")
    print("✅ Demonstrated receipt validation")
    print("✅ Showed batch operations")
    print("✅ Integrated with different agent scenarios")
    print("\n🔐 Each receipt provides:")
    print("   • Cryptographic proof of intent")
    print("   • Tamper-evident audit trail")
    print("   • Time-boxed permissions")
    print("   • Risk context assessment")
    print("   • Agent accountability")
    
    print(f"\n💡 Next steps:")
    print(f"   1. Try the CLI: poi-cli --help")
    print(f"   2. Check examples: python examples/basic_usage.py")
    print(f"   3. Explore LangGraph integration")
    print(f"   4. Customize for your use case")
    
    print(f"\n🚀 You're now ready to build trustworthy AI agents!")


if __name__ == "__main__":
    main()
