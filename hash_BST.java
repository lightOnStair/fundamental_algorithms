class HBST<Key, Value>
{
  private class ValueNode
  {
    private Key key;
    private Value value;
    private ValueNode next;

    public ValueNode(Key key, Value value)
    {
      this.key = key;
      this.value = value;
      this.next = null;
    }
  }

  private class TreeNode
  {
    private int key;
    private ValueNode value;
    private TreeNode left;
    private TreeNode right;

    public TreeNode(int key, ValueNode value)
    {
      this.key = key;
      this.value = value;
      this.left = null;
      this.right = null;
    }
  }

  private TreeNode head;

  public HBST()
  {
    head = new TreeNode(-1,null);
  }


  private int hash(Key key)
  {
    if(key == null)
    {
      return 0;
    }
    else
    {
      return Math.abs(key.hashCode())%35;
    }
  }

  public void put(Key key,Value value)
  {
    int index = hash(key);
    if(head.right==null)
    {
      head.right = new TreeNode(index,new ValueNode(key,value));
    }
    else
    {
      TreeNode temp = head.right;
      while(true)
      {
        if(index<temp.key)
        {
          if(temp.left==null)
          {
            temp.left = new TreeNode(index,new ValueNode(key,value));
            return;
          }
          else
          {
            temp = temp.left;
          }
        }
        else if(index>temp.key)
        {
          if(temp.right==null)
          {
            temp.right = new TreeNode(index,new ValueNode(key,value));
            return;
          }
          else
          {
            temp = temp.right;
          }
        }
        else
        {
          ValueNode temp2 = temp.value;
          while(true)
          {
            if(key == temp2.key)
            {
              temp2.value = value;
              return;
            }
            else if(temp2.next == null)
            {
              temp2.next = new ValueNode(key,value);
              return;
            }
            else
            {
              temp2 = temp2.next;
            }
          }
        }
      }
    }
  }

  public Value get(Key key)
  {
    int index = hash(key);
    if(head.right==null)
    {
      throw new IllegalStateException("it's empty");
    }
    else
    {
      TreeNode temp = head.right;
      while(temp!=null)
      {
        if(index<temp.key)
        {
          temp = temp.left;
        }
        else if(index>temp.key)
        {
          temp = temp.right;
        }
        else
        {
          ValueNode temp2 = temp.value;
          while(temp2!=null)
          {
            if(key == temp2.key)
            {
              return temp2.value;
            }
            else
            {
              temp2 = temp2.next;
            }
          }
          throw new IllegalArgumentException("no such key");
        }
      }
      throw new IllegalArgumentException("no such key");
    }
  }

  public int height()
  {
    return height(head.right);
  }

  private int height(TreeNode root)
  {
    TreeNode subroot = root;
    if(subroot==null)
    {
      return 0;
    }
    else
    {
      return 1 + max(height(subroot.left),height(subroot.right));
    }
  }

  private int max(int m, int n)
  {
    if(m>=n)
    {
      return m;
    }
    else
    {
      return n;
    }
  }
}

class hash_BST
{
  private final static String[] keys =
   { "abstract",     "assert",       "boolean",     "break",
     "byte",         "case",         "catch",       "char",
     "class",        "const",        "continue",    "default",
     "do",           "double",       "else",        "extends",
     "false",        "final",        "finally",     "float",
     "for",          "goto",         "if",          "implements",
     "import",       "instanceof",   "int",         "interface",
     "long",         "native",       "new",         "null",
     "package",      "private",      "protected",   "public",
     "return",       "short",        "static",      "super",
     "switch",       "synchronized", "this",        "throw",
     "throws",       "transient",    "true",        "try",
     "var",          "void",         "volatile",    "while" };

  public static void main(String [] args)
  {
    HBST<String, Integer> hbst = new HBST<String, Integer>();

    for (int index = 0; index < keys.length; index += 1)
    {
      hbst.put(keys[index], index);
    }

    System.out.println(hbst.height());

    for (int index = 0; index < keys.length; index += 1)
    {
      System.out.format("%02d %s", hbst.get(keys[index]), keys[index]);
      System.out.println();
    }
  }
}
