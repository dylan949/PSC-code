from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["shipping_db"]
collection = db["continent_to_continent_routes"]
collection2 = db["port_to_port"]

class ShippingRoutesDB:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="shipping_db", collection_name="continent_to_continent_routes"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def close(self):
        """Close the database connection."""
        self.client.close()
        print("Connection closed")

    def insert_route(self, route):
        """Insert a new shipping route."""
        result = self.collection.insert_one(route)
        print("Route inserted with ID:", result.inserted_id)
        return result.inserted_id

    def find_routes_by_chokepoint(self, chokepoint):
        """Find routes that pass through a specific chokepoint."""
        routes = list(self.collection.find({"choke_points": chokepoint}))
        print("Routes passing through", chokepoint, ":", routes)
        return routes

    def find_high_risk_routes(self, risk_level_threshold):
        """Find high-risk routes based on a given risk level threshold."""
        routes = list(self.collection.find({"risk_level": {"$gt": risk_level_threshold}}))
        print("High-risk routes:", routes)
        return routes

    def update_alternative_route(self, route_id, new_alternative_route):
        """Update the alternative route for a specific shipping route."""
        result = self.collection.update_one(
            {"_id": route_id},
            {"$set": {"alternative_route": new_alternative_route}}
        )
        print(f"Route {route_id} updated. Modified count:", result.modified_count)

    def delete_route(self, route_id):
        """Delete a route by its ID."""
        result = self.collection.delete_one({"_id": route_id})
        print(f"Route {route_id} deleted. Deleted count:", result.deleted_count)

    def find_routes_by_origin_and_destination(self, current_location, final_destination):
        """Find routes between two specific continents."""
        routes = list(self.collection.find({
            "origin_continent": current_location,
            "destination_continent": final_destination
        }))
        print(f"Routes from {current_location} to {final_destination}:", routes)
        return routes

    


