# map-scheduler
That's a simple k8s scheduler based on regular expression mapping

Define a configmap with a yaml mapping regular expressions to node names.

Example:

map-scheduler.yaml
```
test-[0-4]: k8s-worker-node-0
test-[5-9]: k8s-worker-node-1
```

Suppose you create pods test-0, test-1, ..., test-9.

Pods test-0 to test-4 will be scheduled to k8s-worker-node-0, **whether** k8s-worker-node-0 is ready and available to pods requirements.
And pods test-5 to test-9 will be scheduled to k8s-worker-node-1, **whether** k8s-worker-node-1 is ready and available to pods requirements.
If destination nodes are unavailable, pods will persist in *Pending* status.

Use at your own risk. This is not for production use.
