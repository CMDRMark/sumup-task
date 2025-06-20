import pytest

from api_client.url_mapping import BASE_URLS
from utils.logger import logger


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="TEST",
        choices=["LOCAL", "DEV", "TEST", "STAGING", "PROD"],
        help="""Environment to run tests against (e.g. "LOCAL", "DEV", "TEST", "STAGING", "PROD")"""
    )
    parser.addoption(
        "--save-registered-users",
        action="store_true",
        default=False,
        help="Save registered users to a file for later use"
    )


@pytest.fixture(scope='session')
def get_env(request):
    env = request.config.getoption("--env")
    logger.info(f"Running tests in {env} environment")
    return env


@pytest.fixture(scope='session')
def get_base_url(get_env):
    return BASE_URLS[get_env]


@pytest.fixture(scope='session')
def save_registered_users_flag(request):
    yield request.config.getoption("--save-registered-users")



def pytest_collection_modifyitems(config, items):
    env = config.getoption("--env")
    if env == "PROD":
        safe_items = []
        skipped_items = []

        for item in items:
            if "prod_safe" in item.keywords:
                safe_items.append(item)
            else:
                skipped_items.append(item)

        if skipped_items:
            for item in skipped_items:
                item.add_marker(pytest.mark.skip(reason="Unsafe for prod"))

        items[:] = safe_items


# TODO: Fix this
# @pytest.fixture(scope="session", autouse=True)
# def test_stats_collector():
#     stats = {"total": 0, "passed": 0, "failed": 0}
#     yield stats
#
#
# def pytest_runtest_logreport(report):
#     if report.when == "call":
#         stats = pytest.session_stats  # Custom attribute
#         stats["total"] += 1
#         if report.passed:
#             stats["passed"] += 1
#         elif report.failed:
#             stats["failed"] += 1
#
#
# # Attach stats to pytest session object for global access
# def pytest_sessionstart(session):
#     session.stats = {"total": 0, "passed": 0, "failed": 0}
#     pytest.session_stats = session.stats
#
#
# def pytest_html_results_summary(prefix, summary, postfix):
#     stats = pytest.session_stats
#
#     # Create donut chart
#     fig, ax = plt.subplots()
#     sizes = [stats["passed"], stats["failed"]]
#     labels = ["Passed", "Failed"]
#     colors = ["#4CAF50", "#F44336"]
#
#     wedges, texts, autotexts = ax.pie(
#         sizes,
#         labels=labels,
#         colors=colors,
#         autopct="%1.1f%%",
#         startangle=90,
#         pctdistance=0.85
#     )
#
#     # Draw center circle for donut style
#     centre_circle = plt.Circle((0, 0), 0.70, fc='white')
#     fig.gca().add_artist(centre_circle)
#
#     ax.axis('equal')  # Equal aspect ratio ensures a circle.
#     plt.tight_layout()
#
#     # Save to PNG base64
#     buf = io.BytesIO()
#     plt.savefig(buf, format="png")
#     plt.close(fig)
#     buf.seek(0)
#     img_base64 = base64.b64encode(buf.read()).decode('utf-8')
#     img_html = f'<img src="data:image/png;base64,{img_base64}" alt="Test Summary Chart" width="300"/>'
#
#     # Inject chart at top of HTML report
#     prefix.extend([f"<h2>Test Summary</h2>{img_html}"])