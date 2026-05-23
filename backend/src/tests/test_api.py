import pytest
from httpx import ASGITransport, AsyncClient
import pytest_asyncio
from vulnrisk.api.main import app
from vulnrisk.data_sources.nvd import CVEData
from vulnrisk.data_sources.epss import EPSSData


@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


def _sample_cve_data(cve_id: str, cvss_score: float = 8.5) -> CVEData:
    return CVEData(
        {
            "cve_id": cve_id,
            "cvss_score": cvss_score,
            "vulnerability_age_days": 30,
            "cisa_kev": False,
            "has_exploit_references": True,
        }
    )


def _sample_epss_data(cve_id: str, epss_score: float = 0.7) -> EPSSData:
    return EPSSData(
        {
            "cve_id": cve_id,
            "epss_score": epss_score,
            "percentile": 0.9,
        }
    )


@pytest.mark.asyncio
async def test_score_success(async_client):
    class MockNVDClient:
        def __init__(self, api_key=None):
            self.api_key = api_key

        async def get_rich_cve_data(self, cve_id):
            return _sample_cve_data(cve_id)

    class MockEPSSClient:
        def __init__(self, api_key=None):
            self.api_key = api_key

        async def get_rich_epss_data(self, cve_id):
            return _sample_epss_data(cve_id)

    from vulnrisk.api import main

    main.NVDClient = MockNVDClient
    main.EPSSClient = MockEPSSClient

    payload = {
        "cve_id": "CVE-2025-1234",
        "asset_criticality": 9,
        "is_internet_facing": True,
        "framework": "enhanced",
    }
    response = await async_client.post("/api/v1/score", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["cve_id"] == "CVE-2025-1234"
    assert data["priority"] in {"CRITICAL", "HIGH", "MEDIUM", "LOW", "INFORMATIONAL"}
    assert data["risk_score"] > 0
    assert "explanation" in data


@pytest.mark.asyncio
async def test_score_not_found(async_client):
    class MockNVDClient:
        def __init__(self, api_key=None):
            self.api_key = api_key

        async def get_rich_cve_data(self, cve_id):
            return None

    class MockEPSSClient:
        def __init__(self, api_key=None):
            self.api_key = api_key

        async def get_rich_epss_data(self, cve_id):
            return None

    from vulnrisk.api import main

    main.NVDClient = MockNVDClient
    main.EPSSClient = MockEPSSClient

    payload = {
        "cve_id": "CVE-2025-0000",
        "asset_criticality": 5,
        "is_internet_facing": False,
        "framework": "enhanced",
    }
    response = await async_client.post("/api/v1/score", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Vulnerability data not found"
