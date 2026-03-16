#!/usr/bin/env python3
"""Test framework — assertions, fixtures, mocks, test runner."""
import sys, time, traceback

class TestResult:
    def __init__(self): self.passed=0;self.failed=0;self.errors=[];self.duration=0

class Assert:
    @staticmethod
    def equal(a,b,msg=""): assert a==b, msg or f"{a!r} != {b!r}"
    @staticmethod
    def true(v,msg=""): assert v, msg or f"Expected truthy, got {v!r}"
    @staticmethod
    def false(v,msg=""): assert not v, msg or f"Expected falsy, got {v!r}"
    @staticmethod
    def raises(exc_type,fn,*args):
        try: fn(*args); assert False, f"Expected {exc_type.__name__}"
        except exc_type: pass
    @staticmethod
    def near(a,b,tol=1e-6): assert abs(a-b)<tol, f"{a} not near {b}"

class TestSuite:
    def __init__(self,name=""): self.name=name;self.tests=[];self.before=None;self.after=None
    def test(self,name):
        def dec(fn): self.tests.append((name,fn)); return fn
        return dec
    def setup(self,fn): self.before=fn
    def teardown(self,fn): self.after=fn
    def run(self):
        result=TestResult(); start=time.time()
        print(f"\n  Suite: {self.name}")
        for name,fn in self.tests:
            try:
                if self.before: self.before()
                fn(); result.passed+=1; print(f"    ✅ {name}")
                if self.after: self.after()
            except Exception as e:
                result.failed+=1; result.errors.append((name,str(e)))
                print(f"    ❌ {name}: {e}")
        result.duration=time.time()-start
        print(f"  {result.passed} passed, {result.failed} failed ({result.duration:.3f}s)")
        return result

if __name__ == "__main__":
    suite=TestSuite("Math Tests"); a=Assert
    @suite.test("addition")
    def _(): a.equal(2+2,4)
    @suite.test("near")
    def _(): a.near(0.1+0.2,0.3)
    @suite.test("raises")
    def _(): a.raises(ZeroDivisionError,lambda:1/0)
    @suite.test("failing")
    def _(): a.equal(1,2,"intentional fail")
    suite.run()
