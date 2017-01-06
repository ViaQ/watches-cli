# Tutorial

Let's say we want to see **how much JVM heap is used by the Elasticsearch cluster** in total.
This information can be found in `cluster_stats` endpoint.

We can use the `filter` option to get only the relevant slice of the data:
````
$ watches cluster_stats -f nodes.jvm.mem -f timestamp
{
  "timestamp": 1483710714492, 
  "nodes": {
    "jvm": {
      "mem": {
        "heap_used_in_bytes": 89393728, 
        "heap_max_in_bytes": 1038876672
      }
    }
  }
}

````

To turn this output into CVS format we can use `jq`:

````
$ watches cluster_stats -f nodes.jvm.mem -f timestamp |  jq -n -r -f program.jq
1483711201193, 89393728, 1038876672
````

Where the file `program.jq` contains:

````
foreach inputs as $line 
  ( null;
    [
      ($line.timestamp|tostring),
      ($line.nodes.jvm.mem.heap_used_in_bytes|tostring),
      ($line.nodes.jvm.mem.heap_max_in_bytes|tostring)
    ] | join(", ") 
  )
````

Now, to add headers and get more data:

````
$ echo timestamp, heap_used_in_bytes, heap_max_in_bytes; \
  watches cluster_stats -f nodes.jvm.mem -f timestamp -d 10 -i 1 |  jq -n -r -f program.jq
timestamp, heap_used_in_bytes, heap_max_in_bytes
1483711407530, 90468304, 1038876672
1483711408536, 90468304, 1038876672
1483711409545, 91184656, 1038876672
1483711410552, 91184656, 1038876672
1483711411559, 91184656, 1038876672
1483711412567, 91184656, 1038876672
1483711413575, 91184656, 1038876672
1483711414583, 91184656, 1038876672
1483711415592, 91184656, 1038876672
1483711416599, 91184656, 1038876672
````