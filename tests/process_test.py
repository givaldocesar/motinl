from controllers import Process
from methods import Methods

if __name__ == '__main__':
   data = {
        "expression": "x**2 + y**2",
        "x0": [3.0, 3.0],
        "method": Methods.GRADIENTE,
        "alpha": 0.5,
        "tolerance": 0.001,
        "max_iterations": 0,
        "hold_on_graph": True,
        "optimization_type": "min",
        "restrictions": ["x > 2","y > 2"],
        "fast_mode": False
    }
   
   process = Process(data)
   result = process.run()
   print(result)