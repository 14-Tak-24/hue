import data_migration
import pytest
from cryptography.fernet import Fernet
from types import SimpleNamespace


def setup_migrator(tmp_path, monkeypatch):
    monkeypatch.setattr(data_migration, "__file__", str(tmp_path / "data_migration.py"))
    (tmp_path / "exports").mkdir()
    migrator = data_migration.DataMigrationTool()
    migrator.souls_manager = SimpleNamespace(
        get_all_souls=lambda: [
            SimpleNamespace(
                id="soul-1",
                name="Soul One",
                gender="F",
                archetype="Guide",
                rarity="Rare",
                tier="1",
                bio="Migration test",
                voice="Calm",
                email="private@example.test",
                platforms=[],
                tribute_impact="Low",
            )
        ]
    )
    return migrator


def test_postgresql_export_is_encrypted(tmp_path, monkeypatch):
    key = Fernet.generate_key()
    monkeypatch.setenv("MIGRATION_ENCRYPTION_KEY", key.decode())
    migrator = setup_migrator(tmp_path, monkeypatch)

    export_path = migrator.export_for_migration("postgresql")
    with open(export_path, "rb") as export_file:
        encrypted_export = export_file.read()

    assert export_path.endswith(".sql.enc")
    assert b"private@example.test" not in encrypted_export
    assert b"INSERT INTO souls" not in encrypted_export
    assert b"INSERT INTO souls" in Fernet(key).decrypt(encrypted_export)


def test_postgresql_export_requires_encryption_key(tmp_path, monkeypatch):
    monkeypatch.delenv("MIGRATION_ENCRYPTION_KEY", raising=False)
    migrator = setup_migrator(tmp_path, monkeypatch)

    with pytest.raises(ValueError, match="MIGRATION_ENCRYPTION_KEY"):
        migrator.export_for_migration("postgresql")

    assert not list((tmp_path / "exports").iterdir())
