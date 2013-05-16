# coding: utf-8
# This file is part of Thomas Aquinas.
#
# Thomas Aquinas is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Thomas Aquinas is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Thomas Aquinas.  If not, see <http://www.gnu.org/licenses/>.
#
#                       veni, Sancte Spiritus.

from summa import summanode
from nose.tools import ok_, eq_, raises

def test_summanode_add():
    summadad = summanode.SummaNode()
    summachild = summanode.SummaNode()

    summadad.add(summachild, name="summachild")
    ok_(summadad.get_children())

def test_summanode_get():
    summadad = summanode.SummaNode()
    summachild = summanode.SummaNode()

    summadad.add(summachild, name="summachild")
    summaget = summadad.get("summachild")

    ok_(isinstance(summaget, summanode.SummaNode), ("El objeto retornado no es "
                                                    "instancia de  SummaNode"))

def test_summanode_do():
    from summa.actions.interval_actions import Jump
    summachild = summanode.SummaNode()

    saltar = Jump(50, 200, 5, 10)

    summachild.do(saltar)

def test_summanode_remove():
    summadad = summanode.SummaNode()
    summachilda = summanode.SummaNode()
    summachildb = summanode.SummaNode()

    summadad.add(summachilda, name="summachilda")
    summadad.add(summachildb)

    # remove by name
    summadad.remove(summachilda)

    # remove by object
    summadad.remove(summachildb)

def test_summanode_stop():
    from summa.actions.interval_actions import Jump
    summadad = summanode.SummaNode()
    saltar = Jump(50, 200, 5, 10)

    summadad.do(saltar)
    summadad.stop()
