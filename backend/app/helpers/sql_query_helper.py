class SqlHelper:

    @classmethod
    def get_crime_rate_by_district_query(cls):
        return """
            SELECT 
                district_id,
                district_name,
                ROUND(((COUNT(*)::float) / population::float) * 100000) AS crime_rate_per_100k
            FROM crime_data
            GROUP BY district_id, district_name, population
            ORDER BY crime_rate_per_100k DESC
            LIMIT 1
        """
    
    @classmethod
    def get_crimes_by_day_query(cls):
        return """
            SELECT 
                day_of_week,
                COUNT(*) AS crime_count
            FROM crime_data
            GROUP BY day_of_week
            ORDER BY crime_count DESC
            LIMIT 1
        """
    
    @classmethod
    def avg_distance_by_district_query(cls):
        return """
           SELECT 
                district_id,
                district_name,
                Round(AVG(nearest_police_patrol)::NUMERIC, 2) AS avg_patrol_distance
            FROM crime_data
            GROUP BY district_id, district_name
            ORDER BY avg_patrol_distance DESC
            LIMIT 1
        """
    
    @classmethod
    def get_required_stat_query(cls):
        return f"""
            WITH 
                crime_rate_by_district AS (
                    {cls.get_crime_rate_by_district_query()}
                ),
                crimes_by_day AS (
                    {cls.get_crimes_by_day_query()}
                ),
                avg_distance_by_district AS (
                    {cls.avg_distance_by_district_query()}
                ),
                final_results AS (
                    SELECT 
                        'District with Highest Crime Rate' AS metric,
                        district_name AS result,
                        CONCAT(crime_rate_per_100k, ' crimes per 100k') AS value
                    FROM crime_rate_by_district
                    
                    UNION ALL
                    
                    SELECT 
                        'Day with Most Crimes' AS metric,
                        day_of_week AS result,
                        CONCAT(crime_count, ' crimes') AS value
                    FROM crimes_by_day
                    
                    UNION ALL
                    
                    SELECT 
                        'District with Highest Avg Patrol Distance' AS metric,
                        district_name AS result,
                        CONCAT(avg_patrol_distance, ' km') AS value
                    FROM avg_distance_by_district
                )
        SELECT * FROM final_results;
        """