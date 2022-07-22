# Graph Importer
Graph Importer is a tool that helps with importing the data from the Covid-19 Tracking Germany competition from Kaggle into a Neo4j database.  
It inserts the Covid data points as nodes into the database and connects them with relationships.  
To do this, it analyses the Covid Tracking data set and a geospatial file containing the shapes of the german counties,
generating relationships for neighbouring age groups, counties, dates and genders.  

This software suite was developed for the semester assignment of the "Modern Database Systems" lecture of the Software
Engineering Master program at the TH Köln.  
It was developed using techniques and principles of Test Driven Development and Clean Code.

## Getting started
To get started, just edit the server connection parameters and the paths to the case and county files inside
`graphimporter/main.py` and run the main function. This will analyse the provided files and add the nodes and
relationships to your database.

If you want to get a better understanding of the inner workings of the software, take a look into the 
`graphimporter/tests` directory, which contains unit tests covering every aspect of the software suite.

## Nodes and Relationships
Each node contains 8 properties:
- `state`
- `county`
- `age_group`
- `gender`
- `date`
- `cases`
- `deaths`
- `recovered`

4 of these properties are used as coordinates that identify the node on the graph.
Those properties - `age group`, `county`, `date` and `gender` - are the basis for the relationships that connect the nodes.  
Nodes are connected only to their direct neighbours, which are the nodes that differ from the base node only in one of the
4 coordinate properties. This is limited to directly adjacent values of the properties.  
Thus:
- the `age group` relationship only connects nodes with nodes of the next younger and next older age group
- the `county` relationship only connects nodes of neighbouring counties
- the `date` relationship only connects nodes with nodes of the previous and next day
- the `gender` relationship only connects nodes of the other genders (m/f/d)

All relationships are directional, so they have a start and an end node. This allows for easy traversal of the graph in
a set direction. For every relationship, there is a twin relationship of the opposite direction.

The following graphics may be helpful in understanding the constraints on the relationships.

### Age Group Relationships
![](assets/Age%20Group%20Relationship.png)

### Neighbour County Relationships
![](assets/County%20Relationship.png)

### Date Relationships
![](assets/Date%20Relationship.png)

### Gender Relationships
![](assets/Gender%20Relationship.png)

## Data Source
This project uses demographic and geospatial data about the Covid 19 outbreak in Germany from [Kaggle](https://www.kaggle.com/datasets/headsortails/covid19-tracking-germany) as data sources.

## Licence
The demographic data & geospatial shape files are being licensed via the "Data licence Germany – attribution – Version 2.0" available [here](https://www.govdata.de/dl-de/by-2-0).
They were downloaded from https://www.kaggle.com/datasets/headsortails/covid19-tracking-germany.