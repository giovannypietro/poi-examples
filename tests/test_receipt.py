"""
Tests for the PoIReceipt class.
"""

import pytest
from datetime import datetime, timezone, timedelta
from poi_sdk.receipt import PoIReceipt


class TestPoIReceipt:
    """Test cases for PoIReceipt class."""
    
    def test_create_receipt(self):
        """Test creating a receipt with minimal parameters."""
        receipt = PoIReceipt.create(
            agent_id="test_agent",
            action="test_action",
            target_resource="test_resource",
            declared_objective="Test objective"
        )
        
        assert receipt.agent_id == "test_agent"
        assert receipt.action == "test_action"
        assert receipt.target_resource == "test_resource"
        assert receipt.declared_objective == "Test objective"
        assert receipt.receipt_id.startswith("poi_")
        assert receipt.version == "1.0"
        assert receipt.risk_context == "medium"
    
    def test_create_receipt_with_custom_fields(self):
        """Test creating a receipt with custom fields."""
        receipt = PoIReceipt.create(
            agent_id="custom_agent",
            action="custom_action",
            target_resource="custom_resource",
            declared_objective="Custom objective",
            risk_context="high",
            expiration_hours=2.5,
            additional_context={"key": "value"}
        )
        
        assert receipt.risk_context == "high"
        assert receipt.additional_context == {"key": "value"}
        
        # Check expiration time is approximately 2.5 hours from now
        now = datetime.now(timezone.utc)
        expiration = datetime.fromisoformat(receipt.expiration_time.replace('Z', '+00:00'))
        time_diff = (expiration - now).total_seconds()
        assert 9000 <= time_diff <= 9300  # 2.5 hours ± 5 minutes
    
    def test_receipt_validation(self):
        """Test receipt field validation."""
        # Test valid risk context
        receipt = PoIReceipt.create(
            agent_id="test_agent",
            action="test_action",
            target_resource="test_resource",
            declared_objective="Test objective",
            risk_context="low"
        )
        assert receipt.risk_context == "low"
        
        # Test invalid risk context
        with pytest.raises(ValueError, match="Risk context must be one of"):
            PoIReceipt.create(
                agent_id="test_agent",
                action="test_action",
                target_resource="test_resource",
                declared_objective="Test objective",
                risk_context="invalid"
            )
    
    def test_receipt_expiration(self):
        """Test receipt expiration functionality."""
        # Create receipt with short expiration
        receipt = PoIReceipt.create(
            agent_id="test_agent",
            action="test_action",
            target_resource="test_resource",
            declared_objective="Test objective",
            expiration_hours=0.001  # Very short expiration
        )
        
        # Wait a moment and check expiration
        import time
        time.sleep(0.1)  # Wait 100ms
        
        assert receipt.is_expired()
        assert receipt.time_until_expiration() is None
    
    def test_receipt_audit_trail(self):
        """Test adding audit entries to receipt."""
        receipt = PoIReceipt.create(
            agent_id="test_agent",
            action="test_action",
            target_resource="test_resource",
            declared_objective="Test objective"
        )
        
        # Add audit entry
        receipt.add_audit_entry(
            action="receipt_accessed",
            details={"user": "test_user", "timestamp": "2024-01-15T10:00:00Z"}
        )
        
        assert len(receipt.audit_trail) == 1
        assert receipt.audit_trail[0]["action"] == "receipt_accessed"
        assert receipt.audit_trail[0]["details"]["user"] == "test_user"
    
    def test_receipt_compliance_tags(self):
        """Test adding compliance tags to receipt."""
        receipt = PoIReceipt.create(
            agent_id="test_agent",
            action="test_action",
            target_resource="test_resource",
            declared_objective="Test objective"
        )
        
        # Add compliance tags
        receipt.add_compliance_tag("GDPR")
        receipt.add_compliance_tag("SOC2")
        receipt.add_compliance_tag("GDPR")  # Duplicate should not be added
        
        assert len(receipt.compliance_tags) == 2
        assert "GDPR" in receipt.compliance_tags
        assert "SOC2" in receipt.compliance_tags
    
    def test_receipt_signature(self):
        """Test setting signature on receipt."""
        receipt = PoIReceipt.create(
            agent_id="test_agent",
            action="test_action",
            target_resource="test_resource",
            declared_objective="Test objective"
        )
        
        # Set signature
        receipt.set_signature("test_signature_123", "rsa")
        
        assert receipt.signature == "test_signature_123"
        assert receipt.signature_algorithm == "rsa"
    
    def test_receipt_serialization(self):
        """Test receipt serialization methods."""
        receipt = PoIReceipt.create(
            agent_id="test_agent",
            action="test_action",
            target_resource="test_resource",
            declared_objective="Test objective"
        )
        
        # Test to_dict
        receipt_dict = receipt.to_dict()
        assert isinstance(receipt_dict, dict)
        assert receipt_dict["agent_id"] == "test_agent"
        assert receipt_dict["action"] == "test_action"
        
        # Test to_json
        receipt_json = receipt.to_json()
        assert isinstance(receipt_json, str)
        assert "test_agent" in receipt_json
        assert "test_action" in receipt_json
    
    def test_receipt_get_signature_data(self):
        """Test getting signable data from receipt."""
        receipt = PoIReceipt.create(
            agent_id="test_agent",
            action="test_action",
            target_resource="test_resource",
            declared_objective="Test objective"
        )
        
        # Set signature to test exclusion
        receipt.set_signature("test_signature", "rsa")
        
        # Get signable data
        signable_data = receipt.get_signature_data()
        
        # Should not contain signature fields
        assert "signature" not in signable_data
        assert "signature_algorithm" not in signable_data
        assert "certificate_chain" not in signable_data
        
        # Should contain other fields
        assert "agent_id" in signable_data
        assert "action" in signable_data
        assert "target_resource" in signable_data
    
    def test_receipt_string_representation(self):
        """Test string representation of receipt."""
        receipt = PoIReceipt.create(
            agent_id="test_agent",
            action="test_action",
            target_resource="test_resource",
            declared_objective="Test objective"
        )
        
        # Test __str__
        str_repr = str(receipt)
        assert "PoIReceipt" in str_repr
        assert "test_agent" in str_repr
        assert "test_action" in str_repr
        
        # Test __repr__
        repr_repr = repr(receipt)
        assert "PoIReceipt" in repr_repr
        assert "test_agent" in repr_repr
        assert "test_action" in repr_repr
        assert "test_resource" in repr_repr


if __name__ == "__main__":
    pytest.main([__file__])
