from datetime import datetime, timezone

dummy_data = [{
        "click_event_id": 1,
        "label": 0,
        "event_timestamp": datetime(2026, 7, 11, 12, 0, 0, tzinfo=timezone.utc),
        **{f"I{i}": 0.5 for i in range(1, 14)},
        **{f"C{i}": "a1b2c3" for i in range(1, 27)}
    },
    {
        "click_event_id": 2,
        "label": 1,
        "event_timestamp": datetime(2026, 7, 11, 12, 5, 0, tzinfo=timezone.utc),
        **{f"I{i}": 1.2 for i in range(1, 14)},
        **{f"C{i}": "d4e5f6" for i in range(1, 27)}
    },
    {
        "click_event_id": 3,
        "label": 0,
        "event_timestamp": datetime(2026, 7, 11, 12, 10, 0, tzinfo=timezone.utc),
        **{f"I{i}": 3.4 for i in range(1, 14)},
        **{f"C{i}": "g7h8i9" for i in range(1, 27)}
    },
    {
        "click_event_id": 4,
        "label": 0,
        "event_timestamp": datetime(2026, 7, 11, 12, 15, 0, tzinfo=timezone.utc),
        **{f"I{i}": 0.0 for i in range(1, 14)},
        **{f"C{i}": "j0k1l2" for i in range(1, 27)}
    },
    {
        "click_event_id": 5,
        "label": 0,
        "event_timestamp": datetime(2026, 7, 11, 12, 20, 0, tzinfo=timezone.utc),
        **{f"I{i}": 7.8 for i in range(1, 14)},
        **{f"C{i}": "m3n4o5" for i in range(1, 27)}
    },
    {
        "click_event_id": 6,
        "label": 1,
        "event_timestamp": datetime(2026, 7, 11, 12, 25, 0, tzinfo=timezone.utc),
        **{f"I{i}": 5.5 for i in range(1, 14)},
        **{f"C{i}": "p6q7r8" for i in range(1, 27)}
    },
    {
        "click_event_id": 7,
        "label": 0,
        "event_timestamp": datetime(2026, 7, 11, 12, 30, 0, tzinfo=timezone.utc),
        **{f"I{i}": 2.1 for i in range(1, 14)},
        **{f"C{i}": "s9t0u1" for i in range(1, 27)}
    },
    {
        "click_event_id": 8,
        "label": 0,
        "event_timestamp": datetime(2026, 7, 11, 12, 35, 0, tzinfo=timezone.utc),
        **{f"I{i}": 9.3 for i in range(1, 14)},
        **{f"C{i}": "v2w3x4" for i in range(1, 27)}
    },
    {
        "click_event_id": 9,
        "label": 0,
        "event_timestamp": datetime(2026, 7, 11, 12, 40, 0, tzinfo=timezone.utc),
        **{f"I{i}": 4.6 for i in range(1, 14)},
        **{f"C{i}": "y5z6a7" for i in range(1, 27)}
    },
    {
        "click_event_id": 10,
        "label": 1,
        "event_timestamp": datetime(2026, 7, 11, 12, 45, 0, tzinfo=timezone.utc),
        **{f"I{i}": 6.7 for i in range(1, 14)},
        **{f"C{i}": "b8c9d0" for i in range(1, 27)}
    },
    {
        "click_event_id": 11,
        "label": 1,
        "event_timestamp": datetime(2026, 7, 11, 13, 0, 0, tzinfo=timezone.utc),
        **{f"I{i}": 8.9 for i in range(1, 14)},
        **{f"C{i}": "e1f2a3" for i in range(1, 27)}
    },
    {
        "click_event_id": 12,
        "label": 0,
        "event_timestamp": datetime(2026, 7, 11, 13, 5, 0, tzinfo=timezone.utc),
        **{f"I{i}": 0.1 for i in range(1, 14)},
        **{f"C{i}": "b4c5d6" for i in range(1, 27)}
    },
    {
        "click_event_id": 13,
        "label": 0,
        "event_timestamp": datetime(2026, 7, 11, 13, 10, 0, tzinfo=timezone.utc),
        **{f"I{i}": 2.4 for i in range(1, 14)},
        **{f"C{i}": "h7i8j9" for i in range(1, 27)}
    },
    {
        "click_event_id": 14,
        "label": 1,
        "event_timestamp": datetime(2026, 7, 11, 13, 15, 0, tzinfo=timezone.utc),
        **{f"I{i}": 9.9 for i in range(1, 14)},
        **{f"C{i}": "k0l1m2" for i in range(1, 27)}
    },
    {
        "click_event_id": 15,
        "label": 0,
        "event_timestamp": datetime(2026, 7, 11, 13, 20, 0, tzinfo=timezone.utc),
        **{f"I{i}": 4.2 for i in range(1, 14)},
        **{f"C{i}": "n3o4p5" for i in range(1, 27)}
    },
    {
        "click_event_id": 16,
        "label": 0,
        "event_timestamp": datetime(2026, 7, 11, 13, 25, 0, tzinfo=timezone.utc),
        **{f"I{i}": 1.5 for i in range(1, 14)},
        **{f"C{i}": "q6r7s8" for i in range(1, 27)}
    },
    {
        "click_event_id": 17,
        "label": 1,
        "event_timestamp": datetime(2026, 7, 11, 13, 30, 0, tzinfo=timezone.utc),
        **{f"I{i}": 7.3 for i in range(1, 14)},
        **{f"C{i}": "t9u0v1" for i in range(1, 27)}
    },
    {
        "click_event_id": 18,
        "label": 0,
        "event_timestamp": datetime(2026, 7, 11, 13, 35, 0, tzinfo=timezone.utc),
        **{f"I{i}": 3.8 for i in range(1, 14)},
        **{f"C{i}": "w2x3y4" for i in range(1, 27)}
    },
    {
        "click_event_id": 19,
        "label": 0,
        "event_timestamp": datetime(2026, 7, 11, 13, 40, 0, tzinfo=timezone.utc),
        **{f"I{i}": 0.0 for i in range(1, 14)},
        **{f"C{i}": "z5a6b7" for i in range(1, 27)}
    },
    {
        "click_event_id": 20,
        "label": 0,
        "event_timestamp": datetime(2026, 7, 11, 13, 45, 0, tzinfo=timezone.utc),
        **{f"I{i}": 5.1 for i in range(1, 14)},
        **{f"C{i}": "c8d9e0" for i in range(1, 27)}
    }]

dummy_data_missing = [
    {
        "click_event_id": 21,
        "label": 0,
        "event_timestamp": datetime(2026, 7, 11, 14, 0, 0, tzinfo=timezone.utc),
        **{f"I{i}": None if i % 4 == 0 else 0.5 for i in range(1, 14)},  # Missing numerical values
        **{f"C{i}": None if i % 5 == 0 else "a1b2c3" for i in range(1, 27)}  # Missing categorical values
    },
    {
        "click_event_id": 22,
        "label": 1,
        "event_timestamp": datetime(2026, 7, 11, 14, 5, 0, tzinfo=timezone.utc),
        **{f"I{i}": float("nan") if i in [1, 5] else 1.2 for i in range(1, 14)},
        **{f"C{i}": None if i in [2, 6] else "d4e5f6" for i in range(1, 27)}
    },
    {
        "click_event_id": 23,
        "label": 0,
        "event_timestamp": datetime(2026, 7, 11, 14, 10, 0, tzinfo=timezone.utc),
        **{f"I{i}": 3.4 for i in range(1, 14)},
        **{f"C{i}": "g7h8i9" for i in range(1, 27)}
    },
    {
        "click_event_id": 24,
        "label": 0,
        "event_timestamp": datetime(2026, 7, 11, 14, 15, 0, tzinfo=timezone.utc),
        **{f"I{i}": None if i % 2 == 0 else 0.0 for i in range(1, 14)},
        **{f"C{i}": "j0k1l2" for i in range(1, 27)}
    },
    {
        "click_event_id": 25,
        "label": 0,
        "event_timestamp": datetime(2026, 7, 11, 14, 20, 0, tzinfo=timezone.utc),
        **{f"I{i}": 7.8 for i in range(1, 14)},
        **{f"C{i}": None if i % 3 == 0 else "m3n4o5" for i in range(1, 27)}
    },
    {
        "click_event_id": 26,
        "label": 1,
        "event_timestamp": datetime(2026, 7, 11, 14, 25, 0, tzinfo=timezone.utc),
        **{f"I{i}": float("nan") for i in range(1, 14)},  # Completely missing numerical row
        **{f"C{i}": "p6q7r8" for i in range(1, 27)}
    },
    {
        "click_event_id": 27,
        "label": 0,
        "event_timestamp": datetime(2026, 7, 11, 14, 30, 0, tzinfo=timezone.utc),
        **{f"I{i}": 2.1 for i in range(1, 14)},
        **{f"C{i}": None for i in range(1, 27)}  # Completely missing categorical row
    },
    {
        "click_event_id": 28,
        "label": 0,
        "event_timestamp": datetime(2026, 7, 11, 14, 35, 0, tzinfo=timezone.utc),
        **{f"I{i}": None if i > 10 else 9.3 for i in range(1, 14)},
        **{f"C{i}": "v2w3x4" for i in range(1, 27)}
    },
    {
        "click_event_id": 29,
        "label": 0,
        "event_timestamp": datetime(2026, 7, 11, 14, 40, 0, tzinfo=timezone.utc),
        **{f"I{i}": 4.6 for i in range(1, 14)},
        **{f"C{i}": None if i > 20 else "y5z6a7" for i in range(1, 27)}
    },
    {
        "click_event_id": 30,
        "label": 1,
        "event_timestamp": datetime(2026, 7, 11, 14, 45, 0, tzinfo=timezone.utc),
        **{f"I{i}": 6.7 for i in range(1, 14)},
        **{f"C{i}": "b8c9d0" for i in range(1, 27)}
    }
]