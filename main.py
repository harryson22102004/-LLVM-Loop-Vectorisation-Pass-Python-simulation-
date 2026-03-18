import numpy as np, time
 
def scalar_loop(a, b, n):
    c=[0.0]*n
    for i in range(n): c[i]=a[i]+b[i]
    return c
 
def vectorised_loop(a, b): return (np.array(a)+np.array(b)).tolist()
 
def auto_vectorise_analysis(loop_body_str):
    """Analyse if loop can be vectorised (alias, dependency checks)."""
    issues=[]
    if 'c[i-1]' in loop_body_str: issues.append("Loop-carried dependency (c[i] depends on c[i-1])")
    if 'a[b[i]]' in loop_body_str: issues.append("Indirect addressing (possible alias)")
    if 'break' in loop_body_str: issues.append("Early exit prevents vectorisation")
    return {"vectorisable": len(issues)==0, "issues": issues}
 
n=100000; a=list(range(n)); b=list(range(n,2*n))
 
t=time.perf_counter(); cs=scalar_loop(a,b,n); ts=time.perf_counter()-t
t=time.perf_counter(); cv=vectorised_loop(a,b); tv=time.perf_counter()-t
 
print(f"Scalar:     {ts*1000:.2f} ms")
print(f"Vectorised: {tv*1000:.2f} ms")
print(f"Speedup:    {ts/tv:.1f}x")
print(f"Correct:    {cs==cv}")
 
loops=[("c[i]=a[i]+b[i]",{}),("c[i]=c[i-1]+a[i]",{}),("c[i]=a[b[i]]",{})]
for loop,_ in loops:
    r=auto_vectorise_analysis(loop)
    print(f"Loop: {loop[:30]:30s} → {'✓ vectorisable' if r['vectorisable'] else '✗ '+str(r['issues'][0])}")
