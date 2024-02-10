import os
from pathlib import Path

import pytest
from sqlalchemy import exists
from coursework1 import create_app, db
from coursework1.model import Dataset2019
from coursework1.schema import DatasetSchema2019


@pytest.fixture(scope='module')
def app():
    """Fixture that creates a test app.

    The app is created with test config parameters that include a temporary database. The app is created once for
    each test module.

    Returns:
        app A Flask app with a test config
    """

    db_path = Path(__file__).parent.parent.joinpath('instance','test_coursework1.sqlite')
    test_cfg = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': "sqlite:///" + str(db_path),
    }
    app = create_app(test_config=test_cfg)

    
    yield app

    # Clean up / Reset resourcee
    # Delete the test database
    # os.unlink(db_path)


@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def new_dataset(app):
    """Create a new dataset and add to database.
    
    Adds a new dataset to the database and returns an instance of the dataset object.
    """
    new_dataset = {
        "id": 45,
        "location": "NEW",
        "ps_eligible_2019": 100,
        "ps_enroll_2019": 1000,
        "sc_eligible_2019": 100,
        "sc_enroll_2019": 1000
    }

    with app.app_context():
        db.session.add(new_dataset)
        db.session.commit()

    yield new_dataset

    # Remove the region from the database at the end of the test if it still exists
    with app.app_context():
        dataset_exists = db.session.query(exists().where(Dataset2019.id == new_dataset.id)).scalar()
        if dataset_exists:
            db.session.delete(new_dataset)
            db.session.commit()

    