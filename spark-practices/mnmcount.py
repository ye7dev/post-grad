import sys
from pyspark.sql import SparkSession

if __name__ == "__main__":
    if len(sys.argv) != 2:
        # stderr -> 오류 메시지가 일반 출력과 분리
        print('Usage: mnmcount <file>', file=sys.stderr)
        sys.exit(-1)
        
    spark = (SparkSession
             .builder
             .appName('PythonMnMCount')
             .getOrCreate())

    print("SparkSession created")
    
    mnm_file = sys.argv[1]
    print(f"File path provided: {mnm_file}")
    mnm_df = (spark.read.format('csv')
              .option('header', 'true')
              .option('inferSchema', 'true')
              .load(mnm_file))
    
    count_mnm_df = (mnm_df
                    .select('State', 'Color', 'Count')
                    .groupBy('State', 'Color')
                    .sum('Count')
                    .orderBy('sum(Count)', ascending=False))
    
    count_mnm_df.show(n=60, truncate=False)
    print(f'Total Rows = {count_mnm_df.count()}')
    
    # specify state group
    ca_count_mnm_df = (mnm_df
                       .select('State', 'Color', 'Count')
                       .where(mnm_df.State == 'CA')
                       .groupby('State', 'Color')
                       .sum('Count')
                       .orderBy('sum(Count)', ascending=False))
    
    # top 10 results for CA(California)
    ca_count_mnm_df.show(n=10, truncate=False)
    
    spark.stop()
    