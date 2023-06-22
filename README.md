# ZhongjianXu_T2A2

##R1##
This API allows people to query the information about personal hobbies from the database by choosing different categories. 

##R2##
By using this API with our database, people can find those who share same hobbies with them, which can be further used to build interest group online, or combined with location services to schedule offline avtivities.

##R3##
PostgreSQL database was used to structure the data and inentify the relationship among them. As the API functions mainly show the hobbies users share with, so a relational database is suitable for that purpose because the entities are interconnected, and by normalizing the data the database can help to ensure data consistency, thus finding and sorting the data is the advantage of the relational database.
But at the same time, it slows down the performance of the database comparing to non-relational ones.

##R4##
Object-Relational Mapping (ORM) acts as a bridge between relational database and object-oriented programming language.
By using SQLAlchemy in this case, we write python rather than SQL language to interact with the database, which makes data more readable and maintainable. 
The ORM also eliminates the SQL injection by the attackers because we no longer directly write SQL statements.

##R5##


##R6##
'picture' done

##R7##


##R8##





