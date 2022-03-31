from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Tuple, Union

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, Integer, String, asc, cast, desc, inspect, or_
from sqlalchemy.ext import declarative
from sqlalchemy.orm.attributes import InstrumentedAttribute
from werkzeug.exceptions import BadRequest

db = SQLAlchemy(session_options={"autoflush": False})


def declarative_base(cls):
    return declarative.declarative_base(cls=cls)


@declarative_base
class Base(object):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=True,
    )

    def insert(self) -> Base:
        """
        Insert

        :return: Base
        """
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self) -> Base:
        """
        Delete

        :return: Base
        """
        db.session.delete(self)
        db.session.commit()
        return self

    @classmethod
    def update(cls, id: int, to_update: Dict) -> None:
        """
        Update row by id

        :param id:
        :param to_update:
        :return:
        """
        db.session.query(cls).filter(cls.id == id).update(to_update)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id: int) -> Union[Base, None]:
        """
        Get object by id

        :param id:
        :return:
        """
        row = db.session.query(cls).filter_by(id=id).first()
        return row

    @classmethod
    def get(cls) -> Union[Base, None]:
        """

        :return:
        """
        rows = db.session.query(cls).all()
        return rows

    @classmethod
    def modify_query_filter(cls, query: str, args: Dict = {}) -> str:
        """
        Modify query as per the arguments passed in request
        :param args: Dict containing the query args passed in request
        :return: query
        """

        def inspect_field(field: String) -> InstrumentedAttribute:
            if field not in inspect(cls).all_orm_descriptors:
                raise BadRequest({"message": "Invalid field search requested"})
            field = getattr(cls, field)
            return field

        for field, value in args.items():
            # The ordering is important, changing the ordering will break functionality

            if ":neq" in field:
                filter_by = inspect_field(field.split(":")[0])
                query = query.filter(or_(filter_by != val for val in value.split(",")))
            elif ":eq" in field:
                filter_by = inspect_field(field.split(":")[0])
                query = query.filter(or_(filter_by == val for val in value.split(",")))
            elif ":gte" in field:
                filter_by = inspect_field(field.split(":")[0])
                query = query.filter(filter_by >= value)
            elif ":lte" in field:
                filter_by = inspect_field(field.split(":")[0])
                query = query.filter(filter_by <= value)
            elif ":lt" in field:
                filter_by = inspect_field(field.split(":")[0])
                query = query.filter(filter_by < value)
            elif ":gt" in field:
                filter_by = inspect_field(field.split(":")[0])
                query = query.filter(filter_by > value)
            elif ":like" in field:
                filter_by = inspect_field(field.split(":")[0])
                filter_by = cast(filter_by, String)
                query = query.filter(filter_by.ilike("%" + value + "%"))
        return query

    @classmethod
    def modify_query_sort(cls, query: str, args: Dict = {}) -> str:
        """
        Modify query as per the arguments passed in request
        :param args: Dict containing the query args passed in request
        :return: query
        """

        def inspect_field(field: String) -> InstrumentedAttribute:
            if field not in inspect(cls).all_orm_descriptors:
                raise BadRequest({"message": "Invalid field search requested"})
            field = getattr(cls, field)
            return field

        if "order_by" in args:
            for ordering in reversed(args["order_by"].split(",")):
                field, order = ordering.split(":")
                if order == "desc":
                    query = query.order_by(desc(inspect_field(field)))
                else:
                    query = query.order_by(asc(inspect_field(field)))
        else:
            query = query.order_by(desc(inspect_field("updated_at")))
        if "start" in args and "limit" in args and int(args["start"]) > 0:
            query = query.offset((int(args["start"]) - 1) * int(args["limit"]))
            query = query.limit(int(args["limit"]))
        return query

    @classmethod
    def get_queried_list(cls, args: Dict = {}) -> Tuple[List[Base], int]:
        """
        Get list of rows queried from database as per the arguments passed in request
        :param args: Dict containing the query args passed in request
        :return: List of objects of the class on which the function is called and an Int representing length of list
        """

        query = cls.modify_query_filter(db.session.query(cls), args)
        total_rows = query.count()
        query = cls.modify_query_sort(query, args)
        all_rows = query.all()
        return all_rows, total_rows
