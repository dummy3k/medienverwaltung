package dummy.mvapp.search;

import android.app.Activity;
import android.app.ExpandableListActivity;
import android.content.Context;
import android.os.Bundle;
import android.view.ContextMenu;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.*;
import dummy.mvapp.R;

public class ResultsActivity extends ExpandableListActivity {
    private static final String TAG = "ResultsActivity";

    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.results);

        try{
            ExpandableListAdapter mAdapter;
            ExpandableListView epView = (ExpandableListView) findViewById(R.id.ExpandableListView01);
            mAdapter = new MyExpandableListAdapter(this);
            epView.setAdapter(mAdapter);
        }   catch (Exception ex)    {

        }

    }

    public class MyExpandableListAdapter extends BaseExpandableListAdapter {
        // Sample data set. children[i] contains the children (String[]) for
        // groups[i].
        private String[] groups = { "Parent1", "Parent2", "Parent3" };
        private String[][] children = { { "Child1" },{ "Child2" }, { "Child3" },{ "Child4" }, { "Child5" } };
        private Context context;

        public  MyExpandableListAdapter(Context context) {
            this.context =context;
        }
        public Object getChild(int groupPosition, int childPosition) {
            return children[groupPosition][childPosition];
        }

        public long getChildId(int groupPosition, int childPosition) {
            return childPosition;
        }

        public int getChildrenCount(int groupPosition) {
            int i = 0;
            try {
                i = children[groupPosition].length;

            } catch (Exception e) {
            }

            return i;
        }

        public TextView getGenericView() {
            // Layout parameters for the ExpandableListView
            AbsListView.LayoutParams lp = new AbsListView.LayoutParams(
                    ViewGroup.LayoutParams.FILL_PARENT, 64);

            TextView textView = new TextView(context);
            textView.setLayoutParams(lp);
            // Center the text vertically
            textView.setGravity(Gravity.CENTER_VERTICAL | Gravity.LEFT);
//        textView.setTextColor(R.color.marcyred);
            // Set the text starting position
            textView.setPadding(36, 0, 0, 0);
            return textView;
        }

        public View getChildView(int groupPosition, int childPosition,
                                 boolean isLastChild, View convertView, ViewGroup parent) {
            TextView textView = getGenericView();
            textView.setText(getChild(groupPosition, childPosition).toString());
            return textView;
        }

        public Object getGroup(int groupPosition) {
            return groups[groupPosition];
        }

        public int getGroupCount() {
            return groups.length;
        }

        public long getGroupId(int groupPosition) {
            return groupPosition;
        }

        public View getGroupView(int groupPosition, boolean isExpanded,
                                 View convertView, ViewGroup parent) {
            TextView textView = getGenericView();
            textView.setText(getGroup(groupPosition).toString());
            return textView;
        }

        public boolean isChildSelectable(int groupPosition, int childPosition) {
            return true;
        }

        public boolean hasStableIds() {
            return true;
        }

    }

}

