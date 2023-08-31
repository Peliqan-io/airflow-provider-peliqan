__version__ = "1.0.0"
# This is needed to allow Airflow to pick up specific metadata fields
# it needs for certain features.


def get_provider_info():
    return {
            "package-name": "airflow-peliqan-provider",
            "name": "peliqan",
            "description": "A Peliqan Apache Airflow Provider package built with love by Peliqan.",
            "operators": [
                {"integration-name": "peliqan",
                 "python-modules": ["peliqan_provider.operators.peliqan"]}
                ],
            "hooks": [
                {"integration-name": "peliqan",
                 "python-modules": ["peliqan_provider.hooks.peliqan"]}
                ],

            "connection-types": [
                {
                    "connection-type": "peliqan",
                    "hook-class-name": "peliqan_provider.hooks.peliqan.PeliqanHook"
                    }
                ],
            "versions": ["1.0.0"]
            }
