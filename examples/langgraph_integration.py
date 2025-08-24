#!/usr/bin/env python3
"""
LangGraph Integration Example for the Proof-of-Intent SDK.

This example demonstrates how to integrate PoI receipts with LangGraph workflows
to provide cryptographic proof of intent for each step in the workflow.

Requirements:
    pip install langgraph
"""

try:
    from langgraph.graph import StateGraph, END
except ImportError:
    print("LangGraph not installed. Install with: pip install langgraph")
    print("   This example requires LangGraph to run.")
    exit(1)

from poi_sdk import PoIGenerator, PoIValidator, PoIReceipt
from typing import Dict, Any, TypedDict


class PoILangGraphState(TypedDict):
    """State for LangGraph workflow with PoI integration."""
    user_query: str
    poi_receipt: PoIReceipt
    workflow_step: str
    result: str
    error: str


def generate_poi_for_step(state: PoILangGraphState, step_name: str, action: str, resource: str, objective: str) -> PoILangGraphState:
    """
    Generate a PoI receipt for a workflow step.
    
    Args:
        state: Current workflow state
        step_name: Name of the workflow step
        action: Action being performed
        resource: Resource being accessed
        objective: Objective of the action
        
    Returns:
        Updated state with PoI receipt
    """
    print(f"Generating PoI receipt for step: {step_name}")
    
    # Initialize PoI generator
    generator = PoIGenerator()
    
    # Generate receipt for this step
    receipt = generator.generate_receipt(
        agent_id=f"langgraph_workflow_{step_name}",
        action=action,
        target_resource=resource,
        declared_objective=objective,
        risk_context="medium",
        additional_context={
            "workflow_step": step_name,
            "user_query": state.get("user_query", "unknown"),
            "timestamp": state.get("timestamp", "unknown")
        }
    )
    
    print(f"   ✅ PoI receipt generated: {receipt.receipt_id}")
    print(f"   📋 Action: {action}")
    print(f"   🎯 Objective: {objective}")
    
    # Update state
    state["poi_receipt"] = receipt
    state["workflow_step"] = step_name
    
    return state


def analyze_user_query(state: PoILangGraphState) -> PoILangGraphState:
    """Analyze the user query and generate PoI receipt."""
    print("\n📝 Step 1: Analyzing user query...")
    
    # Generate PoI receipt for query analysis
    state = generate_poi_for_step(
        state,
        "query_analysis",
        "text_analysis",
        "user_input",
        "Analyze user query to determine intent and required actions"
    )
    
    # Simulate query analysis
    query = state.get("user_query", "")
    if "database" in query.lower():
        state["result"] = "Query requires database access"
    elif "api" in query.lower():
        state["result"] = "Query requires external API call"
    else:
        state["result"] = "Query requires basic processing"
    
    print(f"   📊 Analysis result: {state['result']}")
    
    return state


def check_permissions(state: PoILangGraphState) -> PoILangGraphState:
    """Check permissions and generate PoI receipt."""
    print("\n🔒 Step 2: Checking permissions...")
    
    # Generate PoI receipt for permission check
    state = generate_poi_for_step(
        state,
        "permission_check",
        "access_control",
        "user_permissions",
        "Verify user has permission to perform requested action"
    )
    
    # Simulate permission check
    query = state.get("user_query", "")
    if "admin" in query.lower():
        state["result"] = "Admin access required - permission denied"
        state["error"] = "Insufficient permissions"
    else:
        state["result"] = "Permission granted"
    
    print(f"   🔐 Permission result: {state['result']}")
    
    return state


def execute_action(state: PoILangGraphState) -> PoILangGraphState:
    """Execute the requested action and generate PoI receipt."""
    print("\n⚡ Step 3: Executing action...")
    
    # Check if we have permission
    if state.get("error"):
        print(f"Skipping execution due to error: {state['error']}")
        return state
    
    # Generate PoI receipt for action execution
    state = generate_poi_for_step(
        state,
        "action_execution",
        "data_operation",
        "target_system",
        "Execute requested action based on user query"
    )
    
    # Simulate action execution
    query = state.get("user_query", "")
    if "database" in query.lower():
        state["result"] = "Database query executed successfully"
    elif "api" in query.lower():
        state["result"] = "API call completed successfully"
    else:
        state["result"] = "Basic processing completed"
    
    print(f"Execution result: {state['result']}")
    
    return state


def generate_response(state: PoILangGraphState) -> PoILangGraphState:
    """Generate response and final PoI receipt."""
    print("Step 4: Generating response...")
    
    # Generate PoI receipt for response generation
    state = generate_poi_for_step(
        state,
        "response_generation",
        "content_generation",
        "response_system",
        "Generate appropriate response for user based on execution results"
    )
    
    # Generate response
    if state.get("error"):
        response = f"Error: {state['error']}"
    else:
        response = f"Success: {state['result']}"
    
    state["result"] = response
    print(f"Response: {response}")
    
    return state


def audit_workflow(state: PoILangGraphState) -> PoILangGraphState:
    """Audit the workflow and add entries to PoI receipts."""
    print("Step 5: Auditing workflow...")
    
    # Get the current receipt
    receipt = state.get("poi_receipt")
    if receipt:
        # Add audit entry for workflow completion
        receipt.add_audit_entry(
            action="workflow_completed",
            details={
                "workflow_steps": ["query_analysis", "permission_check", "action_execution", "response_generation"],
                "final_result": state.get("result", "unknown"),
                "has_errors": bool(state.get("error")),
                "total_steps": 5
            }
        )
        
        print(f"Audit entry added to receipt: {receipt.receipt_id}")
        print(f"Audit trail entries: {len(receipt.audit_trail)}")
    
    return state


def main():
    """Main function to run the LangGraph workflow with PoI integration."""
    print("🔐 LangGraph + PoI SDK Integration Example")
    print("=" * 60)
    
    # Create the workflow
    print("Building LangGraph workflow...")
    
    workflow = StateGraph(PoILangGraphState)
    
    # Add nodes
    workflow.add_node("analyze_query", analyze_user_query)
    workflow.add_node("check_permissions", check_permissions)
    workflow.add_node("execute_action", execute_action)
    workflow.add_node("generate_response", generate_response)
    workflow.add_node("audit_workflow", audit_workflow)
    
    # Add edges
    workflow.add_edge("analyze_query", "check_permissions")
    workflow.add_edge("check_permissions", "execute_action")
    workflow.add_edge("execute_action", "generate_response")
    workflow.add_edge("generate_response", "audit_workflow")
    workflow.add_edge("audit_workflow", END)
    
    # Set entry point
    workflow.set_entry_point("analyze_query")
    
    # Compile the workflow
    app = workflow.compile()
    
    print("Workflow compiled successfully")
    
    # Run the workflow with different queries
    test_queries = [
        "I need to query the user database for customer information",
        "Please call the payment API to process a transaction",
        "I want to access admin functions on the system"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"Running workflow {i}/3 with query: '{query}'")
        print("-" * 60)
        
        # Initialize state
        initial_state = {
            "user_query": query,
            "poi_receipt": None,
            "workflow_step": "",
            "result": "",
            "error": ""
        }
        
        # Run workflow
        try:
            result = app.invoke(initial_state)
            
            print(f"Workflow {i} completed successfully!")
            print(f"   Final result: {result.get('result', 'unknown')}")
            print(f"   Final PoI receipt: {result.get('poi_receipt').receipt_id if result.get('poi_receipt') else 'None'}")
            
            # Validate the final receipt
            if result.get("poi_receipt"):
                validator = PoIValidator()
                try:
                    is_valid = validator.validate_receipt(result["poi_receipt"])
                    print(f"   Receipt validation: {'✅ Valid' if is_valid else '❌ Invalid'}")
                except Exception as e:
                    print(f"   Receipt validation: ❌ Error - {e}")
            
        except Exception as e:
            print(f"   ❌ Workflow failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 LangGraph + PoI integration example completed!")
    print("💡 Each workflow step generated a cryptographically signed PoI receipt")
    print("🔐 This provides provable trust for the entire workflow execution")


if __name__ == "__main__":
    main()
