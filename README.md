# ButterBird
A PyPy script for queuing tweets.

How does it work? It reads tweets from a queue account, and posts them to a main account at a configurable interval. After the tweet has been posted, it is deleted from the queue account.

## Setup

Install [PyPy](http://pypy.org) and [python-twitter](http://code.google.com/p/python-twitter/):

```
brew install pypy
sudo pip install python-twitter
```

1. Make a new application on http://dev.twitter.com
2. Use the `get_access_token.py` scripts to approve the app on your queue and main accounts, and get the access key and secrets for those accounts.
3. Add those values to `bbconfig.py`.
4. `pypy butterbird.py`

## License

```
Copyright (c) 2012 Alex Beal <alexlbeal@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
