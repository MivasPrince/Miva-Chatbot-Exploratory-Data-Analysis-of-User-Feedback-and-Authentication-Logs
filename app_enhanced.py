# Header with logo and title
    st.markdown("""
    <div class="logo-container">
        <img src="data:image/jpeg;base64,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    # Header with logo and title
    st.markdown("""
    <div class="logo-container">
        <img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxAQEhIQEBEWFRUWEBUVFxUYGBYWGBMXGBgWFx4ZFRcYHygiGx4oGxUVIjIiJSorLi8uFyAzOjUtNyguLisBCgoKDg0OGhAQGy0lHyYuNTUrKy0tLS0tLS0tLTArLS0tLS0tLS0vKy0tLS0rLS0tLS0tLS0tNS0tLSs1LS0tK//AABEIAK4BIgMBIgACEQEDEQH/xAAcAAEAAQUBAQAAAAAAAAAAAAAABQECBAYHAwj/xABJEAACAQMBAwkEBwYDBAsAAAABAgADBBESBSExBgcTMkFRYXGxFCJygSM1QlKCkaFidLKztME0U5Izc9HwFSRUY2R1g5TC4fH/xAAaAQEAAwEBAQAAAAAAAAAAAAAAAQIDBAUG/8QAKxEBAAICAQMCBQQDAQAAAAAAAAECAxEEEiExMlEFE0Fh0SJCgbFxoeEz/9oADAMBAAIRAxEAPwDt1Hqr8I9JfLKPVXyHpL4CIiAiIgIiICIiAiIgJZUqBRk8B3DP6CXyA2nUDAFSCDwI3g/OXTV6VXpUF3s99x3vS7Ce3K9jd/f65mzOUlKp7tT6NvHqn59nkZWLwtakxOk5EoDKy6hERAREh9p8oaNHIB1t3A7h8TdkibRHlMRM+EuzAbycCWUawcZXeOw9h8R3jxmuqzOhur5wlFRqFPgvmw7ezAPH9JWw5QantzVBT2qoyW9LtCJTeoaj+YT5alHaZWLbWmkxXq+jZYiJdQiIgIiICIiAiIgIiIEXW6zfEfWUla3Wb4j6ykCSo9VfIekvllHqr5D0l8BERAREQEREBERAREQE4xzi7dfZ+3KF0uSFtKQdfv0y9UMv5bx4gTs84Dz4/WS/udL+OtNMUbtplmnVdtw2nXbZ9wl7aHVbXID6R1WyNRHgcHIPiRwEn61vRv6ftNofe+0nAk9zDsb1mi81+0VvrWtsis3vIDVt2PYM5IHwsc/C5HZLNlbRr7PrkjcVbTUpngwB4H+xnFmj5N9T6Ze7xqRzsG6/wDpX/cff+m2bP2vWtzpByoOCjZ3eA7Vm17M27RrYGdD/dbt+E9vrId6dDaVL2m2OKg3Mp3HP3XHYe49s110IJVgQQcEHiDI6rU+8OC2PczExqYdPkftLaFGhuY5b7g3n593zmmpti4VOjFQ47+0DuDcZgnJPeSfMkn1lrZvZSMXuk9pberVsjOhPur2+Z7ZmbP2dSt0N1dkKqjIU/pkdp7hL7KwpWlP2q7OMbwp7D2bu1vDs9NE5Sbfq31QEghAcU6Y34zuyccWP/0PHO1unvbz7O7h8O3ItqO1Y8ym6V1U2xdBWyltTOtlzj3R948NR/QZmvbL5R/9IcorWoh+hptWpUR2aFoVvex+0cny0jskhy1vBsnZq2SHFzdgmoR9mnuDb/IhB5seyaVzVfW9l8db+nrTu42KYpN7eZcHxDk1vljHj7Ur4/P8vpMSsRKsiIiAiIgIiICIiAiIgRdbrN8R9ZSVrdZviPrKQJKj1V8h6S+WUeqvkPSXwEREBERAREQEREBERATgPPl9ZL+50v46079OA8+X1kv7nS/jrTXD62Wb0tK2NtOpaV6VzS69Nww7j2FT4EEg+BnZeWVrTuqFHaltvSoi6+/fuBI7wfdPkO6cNnVuZTbevptl1hqpujVEGMgdlRT3A5Deee+X5eGMlFvh3Ltxs0WhjbF2tVtKgq0j4Mp6rjub/j2TpC9BtOj01Ahao3MDxB+6/wDZpznlBsprSu9FuAOUb7yHgf7HxE89k7Vq2tQVaLYPAjscdzCeJTJNJ6beH2fM4VOZSMuL1fSff7S2l6LK2gqQ2cacb8zYba1pWNI3V0RqA3LxwewKO1v+fGXUOVFk9H21gA6DSV3awx+yvfnfg92eG+c55Qbcq3tTXUOFGdCDgg/ufGbWtXHG47z9Hj8XgZeRfptHTEefxC/lFt6re1NT+6i50Uwdy+J7z4yZ5B7KQs99XwKVAEgnhqAyWPgo3+eO6axs2xe4qpRpj3nbHkO0nwAyZPc7u1BY2lDZdAECoup276asN2e0s+8+AIPWji45y33Lv+LcmnEwfIxdt/1/1zTldt5toXdW6bIDHTTU/YpruVf7nxYyT5qfray+Ot/T1pqhm181P1tZfHW/p609y0apMfZ8VSd3iZfSgiBE4HcREQEREBERAREQERECLrdZviPrKStbrN8R9ZSBJUeqvkPSXyyj1V8h6S+AiIgIiICIiAiIgIiICcB58vrJf3Ol/HWnfpwHny+sl/c6X8daa4fWyzelz2dx5kOT3Q2731RffrnSmeykp4j4mBPiFWcj5L7Fa+uqNquRrf3mH2EG9m/0g48SJ9S2lslJEp01CoihVUcFUDAA+QmvIt+1lgr3213l5sP2mhrQZq0ssvey9q/3HiPGckn0FOScvNh+zV+kQYp1SWHcrcWX+48/CeRysf74fWfBOZqfkW/j8NZlIk3yT2KbyuqEfRr71Q/sj7PmTu8szjrWbTqH0ObLXFSb28Q3Hm42H0VP2px79QYTwp9/4uPliefO9yd9ssmqouatvmqveU3dIv8ApGrHegm8ooAAAwAMYlWGd09fFHy4iIfA8rNbkXte31fIE2zmp+trL4639PWmPzhcnf8Ao+9q0VGKTfSUvgb7P4WDL5Ad8yOan62svjrf09aejM7pM/Z5lY1fT6UEQInA7iIiAiIgIiICIiAiIgRdbrN8R9ZSVrdZviPrKQJKj1V8h6S+WUeqvkPSXwEREBERAREQEREBERATgPPl9ZL+50v46079OJc5+x3vtuW9qm41LakC33FD1izfJQfnia4p1ZlmjdUzzHcnejo1L9x71b3KfhSU7z+Jx+SDvnVJj2NqlGmlKmulERUUdyqMAfkJkSlrdU7XrXpjRIzlBslbug9FtxIyrfdYcD/z2EyTiUmNxqWlLTS0Wr5hwKtbujtSZSHVyhXt1A4wO/fOv8kNiCzoBSPpG96of2scPIDd+crc8mqT3iXh4qu9exnGNLnyGfyXuk4Jz4cHRMzL1PiHxKeTjrSO3v8A5ViInS8loHPHyc9qszXQZq22ag72pnHSL+QDfg8Zyrmp+trL4q39PWn0k6gjBGR3d84dsXk+dn8o7egB9GXq1KR76bUK+B8iCv4fGb47fpmrDJX9UWdziBEwbkREBERAREQEREBERAi63Wb4j6ykrW6zfEfWUgSVHqr5D0l8so9VfIekvgIiICIiAiIgIiICIiAkNR2Gov6t+29mtqdBB91VZ3Y/Msv+nxkzEBERAREQEREBERASF2tsJa11ZXfB7apUOfvJUpVKZX/UyH5Hvk1EBERAREQEREBERAREQERECLrdZviPrKStbrN8R9ZSBJUeqvkPSXyyj1V8h6S+AiIgIiICImk8uOWB2beWCsfoKorCt+yM0grj4SWJ8CfCTETPaETOvLdolFYHeP8A9lZCSImlcnuWQvNqXVpTYGlRoe7j7bo4Wo2e7Lqo+HPbJiJlEzEN1iIkJIia3y7uLqhaVrq1rBGpUy5VkV1dV3njvBx443cJMRudImdNkicN5L84O1727t7Tp6S9K5BbolOFVWdsDPHSpx4zt1uhVQGYufvEKCfkoA/STak1nUoreLeHpES2qpIIBIOOIxkeIyCJVZdE5LzicptsbLrIFro9GqCabNSXUCuNSvjcTvBzuznhuntzX8sr3aVzUpXNdAEpB1RaaKanvYOSc7hkcN/vDfL/AC56epn8yOrpdUiJrXODtOrZ2VW5o1hTemBpBVXWoSwAUg79+ew7uO+ViN9l5nUbbLE03m9udo3Vul3eVwBU96nSSmi5TsZ2OTv4gDG4j5blExqdETsiJi7TvUt6VSvUOEp02dj4KMyEsqJpPNbytbaVvU6YjpqdU6gPuOSyHyxlfwTdpMxMTqURO43BERISREQERECLrdZviPrKStbrN8R9ZSBJUeqvkPSXyyj1V8h6S+AiIgIiICcG59rjVf0qf3LRTx7Xd+I7Nyr+c7zOMbT2INrbb2nQYgBLMLTb/LqBaGlvH3jUB8CRNcMxFtyyyxuuoTnMxyq9ooew1W+loKNBPF6PAfNdy+RWdLnyps28uNm3a1ACta3qkMh3ZxlWRvAjIz45HZPpjZm3KFxareI4FJqZqFj9gLnUG7ipDA+Rk5aancIxX3Gpa3zscqfYLQpTbFevqppg70XHvVPkCAPFhOX8zNz0e1KS/wCZQq0+OPsip8/9nw/4SVFlU26+0tp1FPRUbWtTtUO7LhGKflnUf2nH3ZqPIG66LaNi/wD4lF/9z6P/AOc0pWOiY+rO1p64l9QRETldRNe5wfq2+/dKv8JmwzXucH6tvv3Sr/CZNfMIt4lwvms+trL46v8AIqz6VnzVzV/W1l8dX+RVn0rNs/qhlg9JERMGzVucjk97fY1aajNVPpaXfrXPuj4lLL+KcA5IbbNjd0LrJ0o/v+NNhpbd2+6Scd4E+qJ8386fJ/2K/qaRilXzWp9wJPvr8m3+TrN8M73WXPmrrVofRqMCAQcgjIPeJzDnLdto39nsamfd1CtcY7F3/qEDnHe6SR5ruU6PsstXffaKyVCf8tBqVv8ARgeamY3NLZPcPd7ZrD37mqy08/ZpKd4HhkKv/pCUiOmZn2Xm3VqIdFt6SoqooAVVCgDgABgAfKesRM2pOZ88m0qtRaGyrYFqtw2tlBwTTp5YD5spPlTM6VVcKCzHAAJJPAAdpnMObkHaO0L3bDj3FboLfPYuBvH4NPzqNL07d1L9+znPNlyh9hvqTs2KVX6Kr3BWPusfJtJ8tU+lp8z85ewfY7+vTAxTqHpqfdpqZJHyfWPICdq5r+UJvrGmztmrSPQ1O8soGGPxKVPmTNc0biLQywzqZrLb4iJzugiIgIiIEXW6zfEfWUla3Wb4j6ykCSo9VfIekvllHqr5D0l8BERAREQKGct5rH6bae2bj/vgoPgalbh8qa/pOhbZvqtFCaNtUrvpOlENNRns1NUZcD8900fmh2Pe2QuUvbZ0arUVxULUmDYBznQ5IOSTwxvl6+mWdvVCF57uSuCu0qK8cJXAHySof0U/hmi7A2ne1aR2RbnK3VdN2/3fveSkBWbwQ95n0rf2dOvTejVUMjoyMp4FWGCJzzmx5DGwubypWBYo/RUHI61MgOXHiQVU9xVh2zSuSOnUqWx/q3DdNj7CpWtotnTGUWkUPYXJB1M2O0kk/OfLtlVNGpTc8aVVGPgUYH1E+tLiroUsFZiB1VxlvAZIH5kT512hze7XqVKrrYOFeo7KDUt8qrMSAfpOwERht52jNWe2n0ajAgEcCMy6QfJW9uXo0kurWpRqrTCuWakysygDKsjsd/HeJOTBvEk17nB+rb790q/wmbDNW5wTc1LSva2tq9Z61LRkNSVEDbiSXcHIGdwB3kSa+YRbw4nzWfW1l8dX+RVn0rOAck+R+17G8t7ttnuwpVCWUVLfJVlZDjNTGcOSPETvNrWLqGKMhP2W06h56SR+s1zTEzGmeHtHd7RETFsTSOdvk97ZYu6Lmrb5qp3lR11HmuTjvUTd5RhndJidTtFo3Gnyxyda5qs1jbNj2w06TniyKSGQ+YBz5TuPIHlDb7QsaNwjAOMJWQfw1lAJx3BhuYcCCO+fOVGqaValqz0lOux65w74znWR3+fzwM+ndj3q3NtRuEOVqUUce9kZIH/HwnRmp6tvmJn3efxuT8i2p8fhQBiRm1NqJb4DKzls7lG7HaSeAHnNCPKFAdN1b3CkH7SYbt7VcMmB2E5PTHpW9vsTYdmrsKCPRqOulqzKNbKxOCXClsnwKg9kmubpTvK2pPtX+W12lvrU0nvqn1Z0NrQi8MJtuovqJG1+V1Nhtm2stBTEKrM5UPg8SvVz5zkfKPb7XblE0r0mPTtuTKOANRSQMOBjdwVv5W7K21VZoUCTi1ePd6R6XT6QfJfr1T28kLNiLOKXSIr71R/dZf8AfJj/ANjA8ZcUi8Z3S/8A7oi7zGfpFsREzOSNq4r+FtQu0J7JR9Ir2nYe4iIoJVGCj5ytPhkdY9qWfbpMYu2eXdOxcpUuaG8FFVM5OcgELqx3+PHhO4cD39uRNcfN+UZJ+VuMzh1sSPYreY/e93JHNEqKKVWEeA0t1qJNV8jMJ1q+a8ZSFSFJLiuxJ/0G2TZ7lIUcfCWgT0i6x7Us+3SYxds8u6di5SpeU75oEZT0igVFJ7J2Huy3FfvMZC4hFfhJBgCJrfOPt1LDZtZ9WKlw3QoOOlh710HlnGO9gJsjGRPKWjTu0uu2rULSnUpVUZHVSrCchcDjBVOaxxF68pE77dL50tr3GzrWlXo1CjUzUYOu4kYHzG/4hO2VXd0YKgZCCqDsKnhOWc7i6tl3Df8AlEH80CfD6k/UfGkj5Nrwi1hS7QYytWbQ1r2p5cFGOlAuFIBLHgQCFzjO7dk9hGJzk7fOzrlKrHNJ8JWAOKlNhlh4MOKeYB7RMJKpWOKJUZLbvz/f7bE1vNiKe2TvMfnXLqp2xjNTF+1IYi3kfmvqLGpWV4hRFtNdPCNLdtdVGKjfqYjTkGkVOLMzgTlflJRO7vSL8K7nQJE7LIXa+0aZlFO1JlQ2tIYKVNH6R7JT6RrnE7ktb3vcrGsrHi7ZJNaxlKAGlcjGUKaeCjFjNLO4Z1NM5HLblDjdS5T0xxl0QSRF0hLfyTH1H7F3p3FQhSJkgAZ6lRJz+CfZzb9oajUW5LBaQY5LDMvePpHyKu1/wBltK/j7rRDZO0lqCYwNPZNTJPdP0j5FXa/7LaV/H3f9K4g4icJNOKKw7kfqfTFj1F+FdSxEdWp7BrGWwm4PKbnxp7qK5Qj+Q7ps8wh1EWFkKOBFOokY3VYukvKKnkAGY1qVtJLMaOXxf7VFtRkOL7nE+TebwQiqPrfBLpkJZ3FAG6eREfz+cGrGUjUjnY3l5dVjGpgPWOq8gOWbYj7YtxgmSP6vNKTFczHWL9Q7JSQKM3HZ+0K1y6rT3InWevuCJnLrqdpJ/QcJoaQFDHJKHEcv19oqPGxKDuMeGz60XKVdSYDjREINmTnb6UntBOhDrwJRfLYSZqlxHVGa7qUfCT/LGvq2hefurf7SYmvKMdcdqjU+wPmP4w5t+VW7Z+0B/8AoVP5JPPj+uy1z6zF2d6e9vQ2lGS5fgT1KgPTr5Ew5CIh7U/8xP5cX6/9KXBfFvxqfCqH7yZ8Y/eeivKTN1aTWa1h8O9KOgCJ6+eLpMOSKF2gBEr2TnHCmhFYu0SihtNEgJyRaLMNO0SlP5sRp7TuPdloTF2Kc/UUi7Z5d07FylOzrGltK0qVaQ6WlVWm6HHu0iWVt2O4cO6dBmh85Gxvbb2yH9pSqBbWop3Y1YqLrPgQWOe0MJtvjtJ9A5ZdaLdJh8OQJyKT13f7r2ftPb57cLuPvNj/qP/ALz6K3YnxD5K5aJekHm87YGnfNdEUO9WlVo1Kb1CvSVlqp0SNUQFkOQy5U5J9Jdl+zGUKyxrNNcSk2vc8mLPpxWN46vw7+06rCNJi6hONa6v4JjUYhVhfAx1Ql7IfZnDSv8AzH+S6tLU17c+vOJ8bpb+GJHKrPJ5qqHyF/iE6z/hjY/V1p8Kn+oTsQnAufnbaWtrbKWAapWYU1JA16KZfh3DUrHzneMGOZPGfkfoLz5XCVRktVEuZi49iJ0wYlb7SLbG0JK7y/E7LLnwx6gB7f4+7LPi7KfLo5X33fU++/8Aov4kZy8+yQOZvtDMLlU8RFFH6N7CJ+0rOlJiZbTvVm82o9U5aHkY4q1LivvmjTqr3nwlaTj7Y/M/xnzaZ+i/hYl1pPy57Y8z+r7hOLOYzklhWqOfDQQO1jbQPpJ8yFOp8Y8VgYfpK9vHJE7Ntz7Pek5L5HJj9s6y2NvJZRdDTQfAP8yXcjyKmjg57J5qQ5l8tHhO8nkdVlbTd+hG7f7zCiE2p0tWNQQRO3Xdp7WmLZZOwLw8Y2qDOVT7cSY2JxXNYyJHVF/KY7LRyWyKgW7zOoKgtm5G/wDmTjJiJdF9kzKl2rHWvtLtpcf8/wB/7MtKnxj78OWfuNqNqjMDiK0WQSFtEpVjGjbfZCBJzJKrmhHKH8Iq8pPZLI6sQy9H8P48LuOZRzPkjv7J+cOyfe7k2TJ8u8et5xOh2Uf7Z5ySd7p0tSNjFVNM5kjtTKKqOwmQwQY1zJEYhyKp3dGnEt2QQFd8k5Z5Tg6lS7dOH9Py8/3LtnKrlHxKlLWpuHDcPnjlMpXfpFMD6u3EsaKJOKVTevylBGhFwRp2jfpVwvKHPYbT7ek5LdDyy7d5Sj8EvOvS/Nf3RDJPK2R8mKO7Fp7evNQb5Hx+qZT4N1GX+FaIhBKJlTSXOiKKsP8A5cVqdsW67uWnLqcOJtEOyft6zBe/K2Fc6dELmhbM6Kzt/8FhBKJKzNBBIxI2Ruz6NsHk7g/6hhWFO2L3O8Jz6b+JX8M2iJM9pAayyaxtfaF5b3O4tF6pNI4bFtfNz7+mTQKKJ8yBVz6b33MzSe7cqtPl6ufI1zW/dZTq1VT33LNn9m3fJ1qtL9PZWuJ6xbUkEqPqWH/AIbKQKQfEz5qO3z6SG1jfDYp+7X+3Jzl7y0g/vV7q3kzfKcnnyh+0LTHF6r+lNzA6CK0+wdaYOJCMZEbNw6KiSWjJZ9NVqJUYTrHr2Fv0j8iW0+HPNkVetZaJiFJUrtMzHMWVfQgj4NfSBzOsHJrq8WPiNbZW02mQrL5j2T5PO3xJepFXf3H9kRaYuO0N4W/FoKSLtjvbtCtLZ9vK9mNPm+zyxONbXrr91qjtT7Wam5rY5Gc7hIYBJ75wQMsJHk/a9HaNJsEvbNcMuwOPJ3o/wCnPWOYdyEaznhNP8r4O9DgLNI5Q2hGCCqVOvaTXMLHH5zXOH7SaVL5EzU1VFIJpV2QJOzJsQAklhEsQT5jfr0I+h6dcv1qE8JXPpwqRGYrDy3YQNJyN1h5M5zv4bE9UWOPbfKWZbmMpEGd/Pj2RTwkrZH0k8P3+/8AKJMZVcnp6gERv+V8JCdPWWQ5zHDyzJHPkjuBuF+OuGWJJIyoJWgdSKhm6xPWjdVRNl1KTwYj7x6yc8p7VbfzSr1Up    # Header with logo
    st.markdown("""
    <div class="logo-container">
        <img src="data:image/jpeg;base64,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 streamlit as st
import pandas as pd
import psycopg2
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pandas.api.types import is_datetime64_any_dtype
import warnings
from datetime import datetime, timedelta
import time
import os
from typing import Dict, Optional, Tuple, List

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Miva AI Database Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Miva branding
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap');
    
    /* Global font family */
    html, body, [class*="css"] {
        font-family: 'Manrope', sans-serif;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e40af;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1.5rem;
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 50%, #f1f5f9 100%);
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        border: 1px solid #e2e8f0;
        font-family: 'Manrope', sans-serif;
    }
    
    .logo-container {
        text-align: center;
        margin-bottom: 1rem;
        padding: 1rem;
    }
    
    .logo-container img {
        max-height: 60px;
        width: auto;
    }
    
    /* Miva color scheme: Blue (#1e40af), Red (#dc2626), Ash (#64748b) */
    .metric-container {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.15);
        margin: 0.5rem 0;
        font-family: 'Manrope', sans-serif;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .status-success {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.15);
    }
    
    .status-error {
        background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.15);
    }
    
    .info-box {
        background: #f8fafc;
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 4px solid #1e40af;
        margin: 1rem 0;
        font-family: 'Manrope', sans-serif;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Sidebar styling with Miva colors */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e40af 0%, #3730a3 100%);
    }
    
    .css-17eq0hr {
        background: linear-gradient(180deg, #1e40af 0%, #3730a3 100%);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-family: 'Manrope', sans-serif;
        font-weight: 500;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3);
    }
    
    /* Primary button styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #b91c1c 0%, #dc2626 100%);
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #f8fafc;
        color: #64748b;
        border-radius: 8px 8px 0 0;
        font-family: 'Manrope', sans-serif;
        font-weight: 500;
        border: 1px solid #e2e8f0;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
    }
    
    /* Metric styling */
    .metric-container .metric-value {
        font-size: 2rem;
        font-weight: 700;
        font-family: 'Manrope', sans-serif;
    }
    
    .metric-container .metric-label {
        font-size: 0.875rem;
        font-weight: 500;
        opacity: 0.9;
        font-family: 'Manrope', sans-serif;
    }
    
    /* Alert styling */
    .stAlert {
        border-radius: 8px;
        font-family: 'Manrope', sans-serif;
    }
    
    .stAlert > div {
        padding-top: 0.75rem;
        padding-bottom: 0.75rem;
    }
    
    /* Success alert */
    .stAlert[data-baseweb="notification"] {
        background-color: #f0fdf4;
        border-left: 4px solid #22c55e;
    }
    
    /* Error alert */
    .stAlert[data-baseweb="notification"][data-testid="stException"] {
        background-color: #fef2f2;
        border-left: 4px solid #dc2626;
    }
    
    /* Warning alert */
    .stAlert[data-baseweb="notification"][data-testid="stWarning"] {
        background-color: #fffbeb;
        border-left: 4px solid #f59e0b;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: #f8fafc;
        border-radius: 8px;
        font-family: 'Manrope', sans-serif;
        font-weight: 600;
    }
    
    /* Selectbox and input styling */
    .stSelectbox > div > div {
        background: white;
        border: 1px solid #d1d5db;
        border-radius: 6px;
        font-family: 'Manrope', sans-serif;
    }
    
    .stTextInput > div > div > input {
        background: white;
        border: 1px solid #d1d5db;
        border-radius: 6px;
        font-family: 'Manrope', sans-serif;
    }
    
    /* Dataframe styling */
    .dataframe {
        font-family: 'Manrope', sans-serif;
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Custom rating button styling */
    .rating-button {
        background: linear-gradient(135deg, #64748b 0%, #94a3b8 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin: 0.25rem;
        font-family: 'Manrope', sans-serif;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .rating-button:hover {
        background: linear-gradient(135deg, #475569 0%, #64748b 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(100, 116, 139, 0.3);
    }
    
    .rating-button.selected {
        background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 2rem;
        background: #f8fafc;
        border-top: 1px solid #e2e8f0;
        margin-top: 3rem;
        font-family: 'Manrope', sans-serif;
        color: #64748b;
    }
    
    /* Sidebar text styling */
    .css-1v3fvcr {
        color: white;
        font-family: 'Manrope', sans-serif;
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        font-family: 'Manrope', sans-serif;
    }
    
    /* Chart container styling */
    .stPlotlyChart {
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class DatabaseConfig:
    """Database configuration management"""
    
    @staticmethod
    def get_config() -> Dict[str, str]:
        """Get database configuration from environment or Streamlit secrets"""
        try:
            # Try Streamlit secrets first (for Streamlit Cloud)
            if hasattr(st, 'secrets') and 'database' in st.secrets:
                return {
                    "host": st.secrets["database"]["host"],
                    "port": st.secrets["database"]["port"],
                    "user": st.secrets["database"]["user"],
                    "password": st.secrets["database"]["password"],
                    "database": st.secrets["database"]["database"]
                }
        except:
            pass
        
        # Fall back to environment variables
        return {
            "host": os.getenv("DB_HOST", "16.170.143.253"),
            "port": int(os.getenv("DB_PORT", "5432")),
            "user": os.getenv("DB_USER", "admin"),
            "password": os.getenv("DB_PASSWORD", "password123"),
            "database": os.getenv("DB_NAME", "miva_ai_db")
        }

class DatabaseManager:
    """Database connection and query management"""
    
    def __init__(self):
        self.config = DatabaseConfig.get_config()
    
    @st.cache_data(ttl=300)
    def test_connection(_self) -> Tuple[bool, str]:
        """Test database connection"""
        try:
            conn = psycopg2.connect(**_self.config)
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            cursor.close()
            conn.close()
            return True, version[0] if version else "Unknown"
        except Exception as e:
            return False, str(e)
    
    @st.cache_data(ttl=300)
    def run_query(_self, query: str) -> List:
        """Execute a query and return results"""
        try:
            conn = psycopg2.connect(**_self.config)
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            st.error(f"Query error: {e}")
            return []
    
    @st.cache_data(ttl=300)
    def query_df(_self, query: str) -> pd.DataFrame:
        """Run a SQL query and return result as Pandas DataFrame"""
        try:
            conn = psycopg2.connect(**_self.config)
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        except Exception as e:
            st.error(f"DataFrame query error: {e}")
            return pd.DataFrame()

class DataProcessor:
    """Data processing utilities"""
    
    @staticmethod
    def try_parse_datetimes(df: pd.DataFrame) -> pd.DataFrame:
        """Auto-parse likely datetime columns"""
        for col in df.columns:
            if df[col].dtype == "object" and any(k in col.lower() for k in ["time","date","at","created","updated"]):
                try:
                    df[col] = pd.to_datetime(df[col], errors="ignore", utc=True)
                except Exception:
                    pass
        return df
    
    @staticmethod
    def get_table_info(db_manager: DatabaseManager) -> pd.DataFrame:
        """Get table information with row counts"""
        try:
            # First try with the correct PostgreSQL system table structure
            query = """
            SELECT 
                schemaname,
                relname as tablename,
                n_tup_ins as inserts,
                n_tup_upd as updates,
                n_tup_del as deletes,
                n_live_tup as live_rows,
                n_dead_tup as dead_rows
            FROM pg_stat_user_tables 
            ORDER BY n_live_tup DESC;
            """
            result = db_manager.query_df(query)
            if not result.empty:
                return result
        except Exception as e:
            print(f"Primary query failed: {e}")
        
        try:
            # Fallback: Simple table list with manual row count
            query = """
            SELECT 
                table_name as tablename,
                (SELECT COUNT(*) FROM information_schema.columns 
                 WHERE table_name = t.table_name AND table_schema = 'public') as column_count
            FROM information_schema.tables t
            WHERE table_schema = 'public'
            ORDER BY table_name;
            """
            return db_manager.query_df(query)
        except Exception as e:
            print(f"Fallback query failed: {e}")
        
        # Final fallback: Just table names
        try:
            tables = db_manager.run_query("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            return pd.DataFrame(tables, columns=['tablename'])
        except:
            return pd.DataFrame()

class CommentAnalyzer:
    """Comment analysis and display utilities"""
    
    @staticmethod
    def get_comments_by_rating(df: pd.DataFrame, rating: int, comment_col: str = 'comment') -> pd.DataFrame:
        """Get comments filtered by rating"""
        if comment_col not in df.columns:
            return pd.DataFrame()
        
        # Filter by rating and remove empty comments
        filtered = df[df['rating'] == rating].copy()
        filtered = filtered[filtered[comment_col].notna() & (filtered[comment_col].str.strip() != '')]
        
        return filtered.sort_values('created_at', ascending=False) if 'created_at' in filtered.columns else filtered
    
    @staticmethod
    def analyze_comment_sentiment(comments: pd.Series) -> dict:
        """Basic sentiment analysis of comments"""
        if comments.empty:
            return {"positive": 0, "negative": 0, "neutral": 0}
        
        # Simple keyword-based sentiment analysis
        positive_words = ['good', 'great', 'excellent', 'amazing', 'love', 'perfect', 'awesome', 'fantastic', 'helpful', 'satisfied']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'poor', 'disappointing', 'useless', 'frustrated', 'annoying', 'slow']
        
        sentiment_scores = []
        for comment in comments:
            if pd.isna(comment):
                continue
            
            comment_lower = str(comment).lower()
            positive_count = sum(1 for word in positive_words if word in comment_lower)
            negative_count = sum(1 for word in negative_words if word in comment_lower)
            
            if positive_count > negative_count:
                sentiment_scores.append('positive')
            elif negative_count > positive_count:
                sentiment_scores.append('negative')
            else:
                sentiment_scores.append('neutral')
        
        total = len(sentiment_scores)
        if total == 0:
            return {"positive": 0, "negative": 0, "neutral": 0}
        
        return {
            "positive": sentiment_scores.count('positive') / total * 100,
            "negative": sentiment_scores.count('negative') / total * 100,
            "neutral": sentiment_scores.count('neutral') / total * 100
        }
    
    @staticmethod
    def get_comment_statistics(df: pd.DataFrame, comment_col: str = 'comment') -> dict:
        """Get basic statistics about comments"""
        if comment_col not in df.columns:
            return {}
        
        comments = df[comment_col].dropna()
        if comments.empty:
            return {}
        
        # Calculate statistics
        lengths = comments.astype(str).str.len()
        word_counts = comments.astype(str).str.split().str.len()
        
        return {
            "total_comments": len(comments),
            "avg_length": lengths.mean(),
            "avg_words": word_counts.mean(),
            "longest_comment": lengths.max(),
            "shortest_comment": lengths.min()
        }

class Visualizer:
    """Visualization utilities using Plotly"""
    
    @staticmethod
    def plot_missing_values(df: pd.DataFrame, title: str):
        """Create interactive missing values plot"""
        na_counts = df.isna().sum()
        na_counts = na_counts[na_counts > 0].sort_values(ascending=False)
        
        if na_counts.empty:
            st.success(f"✅ No missing values in {title}")
            return
        
        fig = px.bar(
            x=na_counts.values,
            y=na_counts.index,
            orientation='h',
            title=f"{title}: Missing Values per Column",
            labels={'x': 'Missing Count', 'y': 'Columns'},
            color=na_counts.values,
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=max(300, 40*len(na_counts)))
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def plot_interactive_rating_distribution(df: pd.DataFrame, col: str, title: str, comment_col: str = 'comment'):
        """Create interactive rating histogram with click functionality"""
        data = df[col].dropna()
        if data.empty:
            st.warning(f"No data in {col}")
            return
        
        # Create rating distribution
        rating_counts = data.value_counts().sort_index()
        
        # Check if comments exist
        has_comments = comment_col in df.columns and not df[comment_col].isna().all()
        
        if has_comments:
            st.markdown("#### 📊 Interactive Rating Distribution")
            st.info("💡 Click on a rating number below to view comments for that rating!")
            
            # Create clickable rating buttons
            st.markdown("##### Select a rating to view comments:")
            cols = st.columns(5)
            
            # Create session state for selected rating if not exists
            if 'selected_rating' not in st.session_state:
                st.session_state.selected_rating = None
            
            # Rating buttons
            for i, rating in enumerate([1, 2, 3, 4, 5]):
                with cols[i]:
                    count = rating_counts.get(rating, 0)
                    if st.button(f"⭐ {rating}\n({count} reviews)", 
                               key=f"rating_{rating}",
                               type="primary" if st.session_state.selected_rating == rating else "secondary"):
                        st.session_state.selected_rating = rating
        
        # Plot the distribution
        fig = px.histogram(
            x=data,
            nbins=5,
            title=f"{title}: Rating Distribution",
            labels={'x': col, 'y': 'Frequency'},
            color_discrete_sequence=['#1f77b4']
        )
        
        # Highlight selected rating if any
        if has_comments and st.session_state.selected_rating is not None:
            fig.add_vline(
                x=st.session_state.selected_rating,
                line_dash="dash",
                line_color="red",
                line_width=3,
                annotation_text=f"Selected: {st.session_state.selected_rating}⭐"
            )
        
        fig.update_layout(
            bargap=0.1, 
            height=400,
            xaxis=dict(dtick=1)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Show comments for selected rating
        if has_comments and st.session_state.selected_rating is not None:
            Visualizer._display_comments_for_rating(
                df, st.session_state.selected_rating, comment_col, title
            )
    
    @staticmethod
    def _display_comments_for_rating(df: pd.DataFrame, rating: int, comment_col: str, title: str):
        """Display comments for a specific rating"""
        comment_analyzer = CommentAnalyzer()
        
        # Get comments for the selected rating
        filtered_comments = comment_analyzer.get_comments_by_rating(df, rating, comment_col)
        
        if filtered_comments.empty:
            st.warning(f"No comments found for {rating}⭐ rating.")
            return
        
        st.markdown(f"### 💬 Comments for {rating}⭐ Rating")
        
        # Comment statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📝 Total Comments", len(filtered_comments))
        
        with col2:
            avg_length = filtered_comments[comment_col].astype(str).str.len().mean()
            st.metric("📏 Avg Length", f"{avg_length:.0f} chars")
        
        with col3:
            if 'created_at' in filtered_comments.columns:
                latest_date = filtered_comments['created_at'].max()
                st.metric("📅 Latest", latest_date.strftime("%m/%d") if pd.notna(latest_date) else "N/A")
        
        with col4:
            unique_users = filtered_comments['email'].nunique() if 'email' in filtered_comments.columns else 0
            st.metric("👥 Unique Users", unique_users)
        
        # Sentiment analysis
        sentiment = comment_analyzer.analyze_comment_sentiment(filtered_comments[comment_col])
        if sentiment:
            st.markdown("#### 🎭 Sentiment Analysis")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("😊 Positive", f"{sentiment['positive']:.1f}%", 
                         delta=f"{sentiment['positive'] - 33.3:.1f}%" if sentiment['positive'] != 33.3 else None)
            with col2:
                st.metric("😐 Neutral", f"{sentiment['neutral']:.1f}%")
            with col3:
                st.metric("😞 Negative", f"{sentiment['negative']:.1f}%",
                         delta=f"{sentiment['negative'] - 33.3:.1f}%" if sentiment['negative'] != 33.3 else None,
                         delta_color="inverse")
        
        # Display comments in an expandable format
        st.markdown("#### 📋 Individual Comments")
        
        # Search/filter functionality
        search_term = st.text_input("🔍 Search in comments:", placeholder="Type to filter comments...")
        
        # Filter comments based on search
        display_comments = filtered_comments
        if search_term:
            mask = display_comments[comment_col].astype(str).str.contains(search_term, case=False, na=False)
            display_comments = display_comments[mask]
            st.info(f"Found {len(display_comments)} comments matching '{search_term}'")
        
        # Pagination
        comments_per_page = 10
        total_comments = len(display_comments)
        total_pages = (total_comments + comments_per_page - 1) // comments_per_page
        
        if total_pages > 1:
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                page = st.selectbox("Page", range(1, total_pages + 1), key=f"page_rating_{rating}")
            
            start_idx = (page - 1) * comments_per_page
            end_idx = min(start_idx + comments_per_page, total_comments)
            display_comments = display_comments.iloc[start_idx:end_idx]
        
        # Display comments
        for idx, row in display_comments.iterrows():
            with st.expander(
                f"💬 Comment #{idx} - {row.get('email', 'Anonymous')} "
                f"({row.get('created_at', 'Unknown date').strftime('%Y-%m-%d %H:%M') if pd.notna(row.get('created_at')) else 'Unknown date'})",
                expanded=False
            ):
                # Comment content
                st.markdown("**Comment:**")
                st.write(row[comment_col])
                
                # Additional metadata in columns
                if any(col in row for col in ['user_agent', 'ip_address', 'email']):
                    st.markdown("**Details:**")
                    detail_cols = st.columns(3)
                    
                    with detail_cols[0]:
                        if 'email' in row and pd.notna(row['email']):
                            st.text(f"📧 {row['email']}")
                    
                    with detail_cols[1]:
                        if 'ip_address' in row and pd.notna(row['ip_address']):
                            st.text(f"🌐 {row['ip_address']}")
                    
                    with detail_cols[2]:
                        if 'created_at' in row and pd.notna(row['created_at']):
                            st.text(f"🕒 {row['created_at'].strftime('%H:%M:%S')}")
        
        # Clear selection button
        if st.button("🔄 Clear Selection", key=f"clear_rating_{rating}"):
            st.session_state.selected_rating = None
            st.experimental_rerun()
    
    @staticmethod
    def plot_rating_distribution(df: pd.DataFrame, col: str, title: str):
        """Create interactive rating histogram"""
        data = df[col].dropna()
        if data.empty:
            st.warning(f"No data in {col}")
            return
        
        # Create histogram with statistics
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=[f"{col} Distribution", "Rating Statistics"],
            specs=[[{"type": "xy"}, {"type": "indicator"}]]
        )
        
        # Histogram
        fig.add_trace(
            go.Histogram(x=data, nbinsx=5, name="Ratings"),
            row=1, col=1
        )
        
        # Statistics
        avg_rating = data.mean()
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=avg_rating,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Average Rating"},
                gauge={
                    'axis': {'range': [None, 5]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 2], 'color': "lightgray"},
                        {'range': [2, 4], 'color': "gray"},
                        {'range': [4, 5], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 4.5
                    }
                }
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            title=f"{title}: {col} Analysis",
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def plot_top_categories(df: pd.DataFrame, col: str, title: str, top_n: int = 20):
        """Create interactive top categories plot"""
        if col not in df.columns:
            st.warning(f"Column '{col}' not found in {title}")
            return
        
        vc = df[col].astype("object").fillna("(Missing)").value_counts().head(top_n)
        if vc.empty:
            st.warning(f"No data in '{col}' for {title}")
            return
        
        fig = px.bar(
            x=vc.values,
            y=vc.index,
            orientation='h',
            title=f"{title}: Top {top_n} {col} Values",
            labels={'x': 'Count', 'y': col},
            color=vc.values,
            color_continuous_scale='Viridis'
        )
        fig.update_layout(
            height=max(400, 30*len(vc)),
            yaxis=dict(categoryorder="total ascending")
        )
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def plot_time_trends(df: pd.DataFrame, title: str, freq: str = "D"):
        """Create interactive time trends plot"""
        time_cols = [c for c in df.columns if is_datetime64_any_dtype(df[c])]
        if not time_cols:
            st.warning(f"No datetime columns detected in {title}")
            return
        
        for col in time_cols:
            s = pd.to_datetime(df[col], errors="coerce", utc=True).dropna()
            if s.empty:
                continue
            
            s = s.dt.tz_convert(None)
            stamped = s.dt.floor(freq)
            counts = stamped.value_counts().sort_index()
            
            if counts.empty:
                continue
            
            # Create line plot with moving average
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=counts.index,
                y=counts.values,
                mode='lines+markers',
                name='Daily Count',
                line=dict(color='#1f77b4', width=2),
                marker=dict(size=4)
            ))
            
            # Add 7-day moving average if enough data
            if len(counts) >= 7:
                ma_7 = counts.rolling(window=7, center=True).mean()
                fig.add_trace(go.Scatter(
                    x=ma_7.index,
                    y=ma_7.values,
                    mode='lines',
                    name='7-day Moving Average',
                    line=dict(color='red', width=2, dash='dash')
                ))
            
            fig.update_layout(
                title=f"{title}: Trends by {col} ({freq})",
                xaxis_title="Time",
                yaxis_title="Count",
                hovermode='x unified',
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)

def create_dashboard():
    """Main dashboard application"""
    # Initialize components
    db_manager = DatabaseManager()
    processor = DataProcessor()
    viz = Visualizer()
    comment_analyzer = CommentAnalyzer()
    
    # Header
    st.markdown('<h1 class="main-header">📊 Miva AI Database Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🔧 Dashboard Controls")
        
        # Connection test
        st.markdown("#### Database Connection")
        if st.button("🔄 Test Connection", type="primary"):
            with st.spinner("Testing connection..."):
                success, info = db_manager.test_connection()
                if success:
                    st.success("✅ Connected successfully!")
                    with st.expander("Connection Details"):
                        st.code(f"Host: {db_manager.config['host']}\nPort: {db_manager.config['port']}\nDatabase: {db_manager.config['database']}")
                        st.info(f"PostgreSQL: {info[:100]}...")
                else:
                    st.error(f"❌ Connection failed")
                    st.error(f"Error: {info}")
        
        # Data management
        st.markdown("#### Data Management")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh"):
                st.cache_data.clear()
                st.success("Cache cleared!")
                st.experimental_rerun()
        
        with col2:
            auto_refresh = st.checkbox("Auto-refresh", help="Refresh data every 5 minutes")
        
        # Analysis options
        st.markdown("#### Analysis Options")
        show_missing = st.checkbox("Missing Values", True)
        show_distributions = st.checkbox("Distributions", True)
        show_trends = st.checkbox("Time Trends", True)
        show_advanced = st.checkbox("Advanced Analytics", False)
        
        # Filters
        st.markdown("#### Filters")
        date_range = st.date_input(
            "Date Range",
            value=(datetime.now() - timedelta(days=30), datetime.now()),
            help="Filter data by date range"
        )
    
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(300)  # 5 minutes
        st.experimental_rerun()
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Overview", 
        "💬 Chat Feedback", 
        "🔐 OTPs", 
        "📊 Custom Analysis",
        "🔍 Advanced Analytics"
    ])
    
    with tab1:
        st.markdown("### Database Overview")
        
        # Get table information
        with st.spinner("Loading database information..."):
            try:
                table_info = processor.get_table_info(db_manager)
                
                if not table_info.empty:
                    # Metrics row
                    col1, col2, col3, col4 = st.columns(4)
                    
                    total_tables = len(table_info)
                    total_rows = table_info.get('live_rows', [0]).sum() if 'live_rows' in table_info.columns else 0
                    
                    with col1:
                        st.metric("📊 Total Tables", total_tables)
                    with col2:
                        st.metric("📈 Total Records", f"{total_rows:,}")
                    with col3:
                        last_update = datetime.now().strftime("%H:%M:%S")
                        st.metric("🕒 Last Updated", last_update)
                    with col4:
                        health_score = "🟢 Healthy" if total_rows > 0 else "🟡 Warning"
                        st.metric("💚 Status", health_score)
                    
                    # Table details
                    st.markdown("### 📋 Table Statistics")
                    
                    if 'live_rows' in table_info.columns:
                        fig = px.bar(
                            table_info,
                            x='tablename',
                            y='live_rows',
                            title="Records per Table",
                            labels={'live_rows': 'Live Records', 'tablename': 'Table Name'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Display table info
                    st.dataframe(table_info, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error loading overview: {e}")
    
    with tab2:
        st.markdown("### 💬 Chat Feedback Analysis")
        
        with st.spinner("Loading chat feedback data..."):
            df_chat = db_manager.query_df("SELECT * FROM chat_feedback;")
            
            if not df_chat.empty:
                df_chat = processor.try_parse_datetimes(df_chat)
                
                # Apply date filter
                if len(date_range) == 2 and 'created_at' in df_chat.columns:
                    mask = (df_chat['created_at'].dt.date >= date_range[0]) & (df_chat['created_at'].dt.date <= date_range[1])
                    df_chat = df_chat.loc[mask]
                
                # Metrics dashboard
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("📊 Total Records", f"{len(df_chat):,}")
                with col2:
                    if 'rating' in df_chat.columns:
                        avg_rating = df_chat['rating'].mean()
                        st.metric("⭐ Average Rating", f"{avg_rating:.2f}")
                with col3:
                    if 'created_at' in df_chat.columns:
                        latest = df_chat['created_at'].max()
                        st.metric("📅 Latest Entry", latest.strftime("%Y-%m-%d") if pd.notna(latest) else "N/A")
                with col4:
                    unique_users = df_chat['email'].nunique() if 'email' in df_chat.columns else 0
                    st.metric("👥 Unique Users", f"{unique_users:,}")
                
                # Analysis sections
                if show_missing:
                    with st.expander("🔍 Missing Values Analysis", expanded=True):
                        viz.plot_missing_values(df_chat, "Chat Feedback")
                
                if show_distributions:
                    with st.expander("📊 Data Distributions", expanded=True):
                        # Interactive Rating Distribution with Comments
                        if 'rating' in df_chat.columns:
                            viz.plot_interactive_rating_distribution(df_chat, 'rating', 'Chat Feedback', 'comment')
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if 'user_agent' in df_chat.columns:
                                viz.plot_top_categories(df_chat, 'user_agent', 'Chat Feedback', 10)
                        with col2:
                            if 'ip_address' in df_chat.columns:
                                viz.plot_top_categories(df_chat, 'ip_address', 'Chat Feedback', 10)
                
                # NEW: Comments Analysis Section
                if 'comment' in df_chat.columns and not df_chat['comment'].isna().all():
                    with st.expander("💬 Comments Analysis", expanded=False):
                        st.markdown("#### 📊 Comment Overview")
                        
                        # Comment statistics
                        comment_stats = comment_analyzer.get_comment_statistics(df_chat, 'comment')
                        if comment_stats:
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                st.metric("📝 Total Comments", f"{comment_stats['total_comments']:,}")
                            with col2:
                                st.metric("📏 Avg Length", f"{comment_stats['avg_length']:.0f} chars")
                            with col3:
                                st.metric("📖 Avg Words", f"{comment_stats['avg_words']:.1f}")
                            with col4:
                                st.metric("📋 Longest", f"{comment_stats['longest_comment']} chars")
                        
                        # Comments by rating breakdown
                        st.markdown("#### 📈 Comments by Rating")
                        comments_by_rating = df_chat.groupby('rating')['comment'].count().reset_index()
                        comments_by_rating.columns = ['Rating', 'Comment Count']
                        
                        fig = px.bar(
                            comments_by_rating,
                            x='Rating',
                            y='Comment Count',
                            title="Number of Comments by Rating",
                            color='Comment Count',
                            color_continuous_scale='Blues'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Recent comments preview
                        st.markdown("#### 🕒 Recent Comments Preview")
                        recent_comments = df_chat[df_chat['comment'].notna()].nlargest(5, 'created_at') if 'created_at' in df_chat.columns else df_chat[df_chat['comment'].notna()].tail(5)
                        
                        for idx, row in recent_comments.iterrows():
                            with st.container():
                                col1, col2 = st.columns([1, 4])
                                with col1:
                                    st.metric("Rating", f"{row['rating']}⭐")
                                with col2:
                                    st.markdown(f"**{row.get('email', 'Anonymous')}** - {row.get('created_at', 'Unknown date')}")
                                    st.write(f"💬 _{row['comment']}_")
                                st.markdown("---")
                
                if show_trends:
                    with st.expander("📈 Time Trends Analysis", expanded=True):
                        viz.plot_time_trends(df_chat, "Chat Feedback")
                
                if show_advanced:
                    with st.expander("🔬 Advanced Analytics", expanded=False):
                        # Rating correlation analysis
                        if 'rating' in df_chat.columns:
                            st.markdown("#### Rating Analysis")
                            
                            # Rating distribution by time of day
                            if 'created_at' in df_chat.columns:
                                df_chat['hour'] = df_chat['created_at'].dt.hour
                                hourly_ratings = df_chat.groupby('hour')['rating'].agg(['mean', 'count']).reset_index()
                                
                                fig = make_subplots(
                                    rows=1, cols=2,
                                    subplot_titles=['Average Rating by Hour', 'Feedback Count by Hour']
                                )
                                
                                fig.add_trace(
                                    go.Bar(x=hourly_ratings['hour'], y=hourly_ratings['mean'], name='Avg Rating'),
                                    row=1, col=1
                                )
                                
                                fig.add_trace(
                                    go.Scatter(x=hourly_ratings['hour'], y=hourly_ratings['count'], 
                                             mode='lines+markers', name='Count'),
                                    row=1, col=2
                                )
                                
                                fig.update_layout(title="Rating Patterns by Hour of Day")
                                st.plotly_chart(fig, use_container_width=True)
                
                # Data export and preview
                with st.expander("📋 Data Preview & Export", expanded=False):
                    st.dataframe(df_chat.head(100), use_container_width=True)
                    
                    # Export options
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        csv = df_chat.to_csv(index=False)
                        st.download_button(
                            label="📥 Download CSV",
                            data=csv,
                            file_name=f"chat_feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                    
                    with col2:
                        json_data = df_chat.to_json(orient='records', date_format='iso')
                        st.download_button(
                            label="📥 Download JSON",
                            data=json_data,
                            file_name=f"chat_feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
                    
                    with col3:
                        # Quick stats
                        st.metric("Rows in Export", len(df_chat))
            else:
                st.warning("No chat feedback data found.")
    
    with tab3:
        st.markdown("### 🔐 OTP Analysis")
        
        with st.spinner("Loading OTP data..."):
            df_otps = db_manager.query_df("SELECT * FROM otps;")
            
            if not df_otps.empty:
                df_otps = processor.try_parse_datetimes(df_otps)
                
                # Apply date filter
                if len(date_range) == 2 and 'created_at' in df_otps.columns:
                    mask = (df_otps['created_at'].dt.date >= date_range[0]) & (df_otps['created_at'].dt.date <= date_range[1])
                    df_otps = df_otps.loc[mask]
                
                # Metrics dashboard
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("📊 Total OTPs", f"{len(df_otps):,}")
                with col2:
                    if 'otp_code' in df_otps.columns:
                        avg_length = df_otps['otp_code'].astype(str).str.len().mean()
                        st.metric("📏 Avg Length", f"{avg_length:.1f}")
                with col3:
                    if 'used' in df_otps.columns:
                        used_rate = df_otps['used'].mean() * 100
                        st.metric("✅ Usage Rate", f"{used_rate:.1f}%")
                with col4:
                    unique_emails = df_otps['email'].nunique() if 'email' in df_otps.columns else 0
                    st.metric("👥 Unique Users", f"{unique_emails:,}")
                
                # Analysis sections
                if show_missing:
                    with st.expander("🔍 Missing Values Analysis", expanded=True):
                        viz.plot_missing_values(df_otps, "OTPs")
                
                if show_distributions:
                    with st.expander("📊 Data Distributions", expanded=True):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # OTP length distribution
                            if 'otp_code' in df_otps.columns:
                                lengths = df_otps['otp_code'].dropna().astype(str).str.len()
                                if not lengths.empty:
                                    fig = px.histogram(
                                        x=lengths,
                                        title="OTP Code Length Distribution",
                                        labels={'x': 'Length', 'y': 'Frequency'},
                                        nbins=10
                                    )
                                    st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            # Usage status distribution
                            if 'used' in df_otps.columns:
                                status_counts = df_otps['used'].value_counts()
                                fig = px.pie(
                                    values=status_counts.values,
                                    names=['Used' if x else 'Unused' for x in status_counts.index],
                                    title="OTP Usage Status",
                                    color_discrete_sequence=['#ff7f0e', '#1f77b4']
                                )
                                st.plotly_chart(fig, use_container_width=True)
                        
                        # Email domain analysis
                        if 'email' in df_otps.columns:
                            df_otps['email_domain'] = df_otps['email'].str.split('@').str[1]
                            viz.plot_top_categories(df_otps, 'email_domain', 'OTPs', 15)
                
                if show_trends:
                    with st.expander("📈 Time Trends Analysis", expanded=True):
                        viz.plot_time_trends(df_otps, "OTPs")
                
                if show_advanced:
                    with st.expander("🔬 Advanced Analytics", expanded=False):
                        # Usage patterns
                        if 'used' in df_otps.columns and 'created_at' in df_otps.columns:
                            st.markdown("#### Usage Patterns")
                            
                            # Usage rate over time
                            df_otps['date'] = df_otps['created_at'].dt.date
                            daily_usage = df_otps.groupby('date').agg({
                                'used': ['sum', 'count', 'mean']
                            }).reset_index()
                            daily_usage.columns = ['date', 'used_count', 'total_count', 'usage_rate']
                            
                            fig = make_subplots(
                                rows=2, cols=1,
                                subplot_titles=['Daily OTP Generation vs Usage', 'Daily Usage Rate'],
                                shared_xaxes=True
                            )
                            
                            fig.add_trace(
                                go.Bar(x=daily_usage['date'], y=daily_usage['total_count'], 
                                      name='Generated', marker_color='lightblue'),
                                row=1, col=1
                            )
                            
                            fig.add_trace(
                                go.Bar(x=daily_usage['date'], y=daily_usage['used_count'], 
                                      name='Used', marker_color='darkblue'),
                                row=1, col=1
                            )
                            
                            fig.add_trace(
                                go.Scatter(x=daily_usage['date'], y=daily_usage['usage_rate'] * 100, 
                                          mode='lines+markers', name='Usage Rate (%)',
                                          line=dict(color='red', width=2)),
                                row=2, col=1
                            )
                            
                            fig.update_layout(
                                title="OTP Usage Analysis Over Time",
                                height=600,
                                showlegend=True
                            )
                            st.plotly_chart(fig, use_container_width=True)
                
                # Data export and preview
                with st.expander("📋 Data Preview & Export", expanded=False):
                    st.dataframe(df_otps.head(100), use_container_width=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        csv = df_otps.to_csv(index=False)
                        st.download_button(
                            label="📥 Download CSV",
                            data=csv,
                            file_name=f"otps_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                    
                    with col2:
                        json_data = df_otps.to_json(orient='records', date_format='iso')
                        st.download_button(
                            label="📥 Download JSON",
                            data=json_data,
                            file_name=f"otps_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
                    
                    with col3:
                        st.metric("Rows in Export", len(df_otps))
            else:
                st.warning("No OTP data found.")
    
    with tab4:
        st.markdown("### 📊 Custom SQL Analysis")
        
        # Query templates
        st.markdown("#### 📝 Query Templates")
        template_options = {
            "Select All Chat Feedback": "SELECT * FROM chat_feedback LIMIT 100;",
            "Top Rated Feedback": "SELECT * FROM chat_feedback WHERE rating = 5 ORDER BY created_at DESC LIMIT 20;",
            "OTP Usage by Email Domain": """
                SELECT 
                    SPLIT_PART(email, '@', 2) as domain,
                    COUNT(*) as total_otps,
                    SUM(CASE WHEN used = true THEN 1 ELSE 0 END) as used_otps,
                    ROUND(AVG(CASE WHEN used = true THEN 1.0 ELSE 0.0 END) * 100, 2) as usage_rate
                FROM otps 
                GROUP BY domain 
                ORDER BY total_otps DESC
                LIMIT 10;
            """,
            "Daily Feedback Trends": """
                SELECT 
                    DATE(created_at) as date,
                    COUNT(*) as feedback_count,
                    AVG(rating) as avg_rating
                FROM chat_feedback 
                WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
                GROUP BY DATE(created_at) 
                ORDER BY date DESC;
            """,
            "User Engagement Analysis": """
                SELECT 
                    cf.email,
                    COUNT(cf.id) as feedback_count,
                    AVG(cf.rating) as avg_rating,
                    COUNT(o.id) as otp_count,
                    MAX(cf.created_at) as last_feedback
                FROM chat_feedback cf
                LEFT JOIN otps o ON cf.email = o.email
                GROUP BY cf.email
                HAVING COUNT(cf.id) > 1
                ORDER BY feedback_count DESC
                LIMIT 20;
            """
        }
        
        selected_template = st.selectbox(
            "Choose a template:",
            options=list(template_options.keys()),
            index=0
        )
        
        # Query input
        query = st.text_area(
            "SQL Query:",
            value=template_options[selected_template],
            height=200,
            help="Write your SQL query here. Be careful with large result sets!"
        )
        
        # Query execution
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if st.button("🚀 Execute Query", type="primary"):
                if query.strip():
                    with st.spinner("Executing query..."):
                        try:
                            start_time = time.time()
                            result_df = db_manager.query_df(query)
                            execution_time = time.time() - start_time
                            
                            if not result_df.empty:
                                st.success(f"✅ Query executed successfully! {len(result_df)} rows returned in {execution_time:.2f}s")
                                
                                # Display results with pagination
                                if len(result_df) > 1000:
                                    st.warning("⚠️ Large result set detected. Showing first 1000 rows.")
                                    display_df = result_df.head(1000)
                                else:
                                    display_df = result_df
                                
                                st.dataframe(display_df, use_container_width=True)
                                
                                # Quick statistics
                                if len(result_df.select_dtypes(include=[np.number]).columns) > 0:
                                    st.markdown("#### 📊 Quick Statistics")
                                    st.dataframe(result_df.describe(), use_container_width=True)
                                
                                # Download results
                                col1, col2 = st.columns(2)
                                with col1:
                                    csv = result_df.to_csv(index=False)
                                    st.download_button(
                                        label="📥 Download Results (CSV)",
                                        data=csv,
                                        file_name=f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                        mime="text/csv"
                                    )
                                
                                with col2:
                                    json_data = result_df.to_json(orient='records', date_format='iso')
                                    st.download_button(
                                        label="📥 Download Results (JSON)",
                                        data=json_data,
                                        file_name=f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                        mime="application/json"
                                    )
                            else:
                                st.info("Query executed successfully but returned no results.")
                                
                        except Exception as e:
                            st.error(f"❌ Query execution failed: {e}")
                else:
                    st.warning("Please enter a SQL query.")
        
        with col2:
            if st.button("🔄 Clear Query"):
                st.experimental_rerun()
        
        with col3:
            if st.button("💾 Save Query"):
                st.info("Query saving feature coming soon!")
    
    with tab5:
        if show_advanced:
            st.markdown("### 🔍 Advanced Analytics")
            
            # Cross-table analysis
            st.markdown("#### 🔗 Cross-Table Analysis")
            
            with st.spinner("Loading cross-table analysis..."):
                try:
                    # User engagement correlation - Updated for correct OTP table structure
                    try:
                        # Since OTP table uses user_id instead of email, we need a different approach
                        st.info("📊 Note: OTP table uses user_id rather than email. Showing separate analysis for each table.")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("#### 💬 Chat Feedback Analysis")
                            feedback_analysis = db_manager.query_df("""
                                SELECT 
                                    COUNT(*) as total_feedback,
                                    ROUND(AVG(rating), 2) as avg_rating,
                                    COUNT(DISTINCT email) as unique_users,
                                    COUNT(CASE WHEN rating >= 4 THEN 1 END) as positive_feedback,
                                    COUNT(CASE WHEN rating <= 2 THEN 1 END) as negative_feedback
                                FROM chat_feedback
                                WHERE created_at >= CURRENT_DATE - INTERVAL '30 days';
                            """)
                            
                            if not feedback_analysis.empty:
                                for _, row in feedback_analysis.iterrows():
                                    st.metric("Total Feedback", f"{row['total_feedback']:,}")
                                    st.metric("Average Rating", f"{row['avg_rating']}/5")
                                    st.metric("Unique Users", f"{row['unique_users']:,}")
                                    positive_pct = (row['positive_feedback'] / row['total_feedback'] * 100) if row['total_feedback'] > 0 else 0
                                    st.metric("Positive Rate", f"{positive_pct:.1f}%")
                        
                        with col2:
                            st.markdown("#### 🔐 OTP Analysis")
                            otp_analysis = db_manager.query_df("""
                                SELECT 
                                    COUNT(*) as total_otps,
                                    COUNT(DISTINCT user_id) as unique_users,
                                    ROUND(AVG(CASE WHEN is_used = true THEN 1.0 ELSE 0.0 END) * 100, 1) as usage_rate,
                                    COUNT(CASE WHEN is_used = true THEN 1 END) as used_otps,
                                    COUNT(CASE WHEN is_used = false THEN 1 END) as unused_otps
                                FROM otps
                                WHERE created_at >= CURRENT_DATE - INTERVAL '30 days';
                            """)
                            
                            if not otp_analysis.empty:
                                for _, row in otp_analysis.iterrows():
                                    st.metric("Total OTPs", f"{row['total_otps']:,}")
                                    st.metric("Unique Users", f"{row['unique_users']:,}")
                                    st.metric("Usage Rate", f"{row['usage_rate']}%")
                                    st.metric("Used OTPs", f"{row['used_otps']:,}")
                        
                        # Daily trends comparison
                        st.markdown("#### 📈 Daily Activity Comparison")
                        
                        daily_trends = db_manager.query_df("""
                            WITH feedback_daily AS (
                                SELECT 
                                    DATE(created_at) as date,
                                    COUNT(*) as feedback_count,
                                    AVG(rating) as avg_rating
                                FROM chat_feedback
                                WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
                                GROUP BY DATE(created_at)
                            ),
                            otp_daily AS (
                                SELECT 
                                    DATE(created_at) as date,
                                    COUNT(*) as otp_count,
                                    ROUND(AVG(CASE WHEN is_used = true THEN 1.0 ELSE 0.0 END) * 100, 1) as usage_rate
                                FROM otps
                                WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
                                GROUP BY DATE(created_at)
                            )
                            SELECT 
                                COALESCE(f.date, o.date) as date,
                                COALESCE(f.feedback_count, 0) as feedback_count,
                                COALESCE(f.avg_rating, 0) as avg_rating,
                                COALESCE(o.otp_count, 0) as otp_count,
                                COALESCE(o.usage_rate, 0) as usage_rate
                            FROM feedback_daily f
                            FULL OUTER JOIN otp_daily o ON f.date = o.date
                            ORDER BY date DESC
                            LIMIT 30;
                        """)
                        
                        if not daily_trends.empty:
                            # Create comparison chart
                            fig = make_subplots(
                                rows=2, cols=2,
                                subplot_titles=['Daily Feedback Count', 'Daily Average Rating', 'Daily OTP Count', 'Daily OTP Usage Rate'],
                                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                                      [{"secondary_y": False}, {"secondary_y": False}]]
                            )
                            
                            # Feedback count
                            fig.add_trace(
                                go.Scatter(x=daily_trends['date'], y=daily_trends['feedback_count'], 
                                          mode='lines+markers', name='Feedback Count', line=dict(color='blue')),
                                row=1, col=1
                            )
                            
                            # Average rating
                            fig.add_trace(
                                go.Scatter(x=daily_trends['date'], y=daily_trends['avg_rating'], 
                                          mode='lines+markers', name='Avg Rating', line=dict(color='green')),
                                row=1, col=2
                            )
                            
                            # OTP count
                            fig.add_trace(
                                go.Scatter(x=daily_trends['date'], y=daily_trends['otp_count'], 
                                          mode='lines+markers', name='OTP Count', line=dict(color='orange')),
                                row=2, col=1
                            )
                            
                            # OTP usage rate
                            fig.add_trace(
                                go.Scatter(x=daily_trends['date'], y=daily_trends['usage_rate'], 
                                          mode='lines+markers', name='Usage Rate %', line=dict(color='red')),
                                row=2, col=2
                            )
                            
                            fig.update_layout(
                                title="30-Day Activity Trends Comparison",
                                height=600,
                                showlegend=False
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Summary insights
                            st.markdown("#### 💡 Key Insights")
                            
                            # Calculate some basic insights
                            avg_feedback_per_day = daily_trends['feedback_count'].mean()
                            avg_otp_per_day = daily_trends['otp_count'].mean()
                            avg_usage_rate = daily_trends['usage_rate'].mean()
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Avg Daily Feedback", f"{avg_feedback_per_day:.1f}")
                            with col2:
                                st.metric("Avg Daily OTPs", f"{avg_otp_per_day:.1f}")
                            with col3:
                                st.metric("Avg Usage Rate", f"{avg_usage_rate:.1f}%")
                        
                        return  # Exit since we're showing alternative analysis
                        
                    except Exception as e:
                        st.error(f"Error in advanced analysis: {e}")
                        return
                    
                    correlation_df = None  # This won't be reached
                    
                    if not correlation_df.empty:
                        # Scatter plot: feedback vs OTP usage
                        fig = px.scatter(
                            correlation_df,
                            x='feedback_count',
                            y='otp_count',
                            color='avg_rating',
                            size='otp_usage_rate',
                            hover_data=['email'],
                            title="User Engagement: Feedback vs OTP Usage",
                            labels={
                                'feedback_count': 'Number of Feedback',
                                'otp_count': 'Number of OTPs',
                                'avg_rating': 'Average Rating'
                            }
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Correlation matrix
                        numeric_cols = ['feedback_count', 'avg_rating', 'otp_count', 'otp_usage_rate']
                        corr_matrix = correlation_df[numeric_cols].corr()
                        
                        fig_corr = px.imshow(
                            corr_matrix,
                            title="Correlation Matrix: User Engagement Metrics",
                            aspect="auto",
                            color_continuous_scale="RdBu"
                        )
                        st.plotly_chart(fig_corr, use_container_width=True)
                        
                        # Top users
                        st.markdown("#### 🏆 Top Engaged Users")
                        top_users = correlation_df.nlargest(10, 'feedback_count')
                        st.dataframe(top_users, use_container_width=True)
                
                except Exception as e:
                    st.error(f"Error in cross-table analysis: {e}")
        else:
            st.info("Enable 'Advanced Analytics' in the sidebar to see this section.")
    
    # Footer with system info
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"**🕒 Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    with col2:
        st.markdown(f"**🗄️ Database:** {db_manager.config['host']}")
    
    with col3:
        if st.button("ℹ️ System Info"):
            st.info(f"""
            **System Information:**
            - Python: {pd.__version__}
            - Pandas: {pd.__version__}
            - Streamlit: {st.__version__}
            - Database: PostgreSQL
            """)

# Application entry point
def main():
    """Main application entry point"""
    try:
        create_dashboard()
    except Exception as e:
        st.error(f"Application Error: {e}")
        st.info("Please check your database connection and try refreshing the page.")

if __name__ == "__main__":
    main()
