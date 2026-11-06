import unittest
from unittest.mock import AsyncMock, patch

import main


class MainTests(unittest.IsolatedAsyncioTestCase):
    async def test_main_awaits_runner_with_configured_count(self):
        with patch.object(main, "NUM_BATTLES", 7):
            with patch.object(main, "run_battles", new_callable=AsyncMock) as runner:
                await main.main()
                runner.assert_awaited_once_with(7)
