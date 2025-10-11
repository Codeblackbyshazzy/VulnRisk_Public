import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest_asyncio
from vulnrisk.api.main import app

import asyncio

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_score_success(monkeypatch, async_client):
    # Mock NVDClient and EPSSClient to avoid real API calls
    class MockNVDClient:
        async def get_cvss_score(self, cve_id):
            return 8.5
    class MockEPSSClient:
        async def get_epss_score(self, cve_id):
            return 0.7
    # Patch the clients in the endpoint
    from vulnrisk.api import main
    main.NVDClient = lambda: MockNVDClient()
    main.EPSSClient = lambda: MockEPSSClient()

    payload = {
        "cve_id": "CVE-2025-1234",
        "asset_criticality": 9,
        "is_internet_facing": True,
        "framework": "enhanced"
    }
    response = await async_client.post("/api/v1/score", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["cve_id"] == "CVE-2025-1234"
    assert data["priority"] == "CRITICAL"
    assert data["risk_score"] > 15
    assert "explanation" in data

@pytest.mark.asyncio
async def test_score_not_found(monkeypatch, async_client):
    class MockNVDClient:
        async def get_cvss_score(self, cve_id):
            return None
    class MockEPSSClient:
        async def get_epss_score(self, cve_id):
            return None
    from vulnrisk.api import main
    main.NVDClient = lambda: MockNVDClient()
    main.EPSSClient = lambda: MockEPSSClient()

    payload = {
        "cve_id": "CVE-2025-0000",
        "asset_criticality": 5,
        "is_internet_facing": False,
        "framework": "enhanced"
    }
    response = await async_client.post("/api/v1/score", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Vulnerability data not found" 