"""BusinessInfinity — purpose-driven boardroom on the Agent Operating System.

BusinessInfinity is a living boardroom of legendary CXO agents.  Each agent
inherits the company's purpose, responds to events with domain leadership,
and debates through a decision tree of pathways.  Resonance scoring ensures
debates converge in seconds, and autonomous actions are taken with purpose
front and centre.

The ``aos-client-sdk`` provides the ``AOSApp`` framework that handles all
Azure Functions scaffolding, Service Bus communication, authentication,
and deployment.  BusinessInfinity just defines workflows.

Usage::

    from business_infinity.workflows import app

    # function_app.py:
    functions = app.get_functions()
"""

__version__ = "5.0.0"
