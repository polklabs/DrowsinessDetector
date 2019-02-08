using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Data.SqlClient;
using System.Web.UI.WebControls;

namespace WebAppEx
{
    public partial class Statistics : Page
    {
        string DrowsyMin;
        SqlConnection con = new SqlConnection(@"Data Source=(LocalDB)\MSSQLLocalDB;AttachDbFilename=C:\Users\uidh2591\Documents\Visual Studio 2015\Projects\WebAppEx\WebAppEx\App_Data\aspnet-WebAppEx-20190115082250.mdf;Integrated Security=True");

        protected void Page_Load(object sender, EventArgs e)
        {
            string UserID = (string)(Session["UserID"]);
            System.Diagnostics.Debug.Write("Value of UserID: " + UserID);

            if (UserID == null || UserID == "")
            {
                Response.Write("<script language='javascript'>alert('Please log in first.');</script>");
                Server.Transfer("\\Account\\Login.aspx", true);
            }
            else
            {
                con.Open();
                SqlCommand cmd = con.CreateCommand();
                cmd.CommandType = System.Data.CommandType.Text;
                string query = "SELECT DrowsyMin FROM UserData WHERE UserID = @UserID";
                cmd.Parameters.AddWithValue("@UserID", UserID);
                cmd.CommandText = query;
                using (SqlDataReader reader = cmd.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        DrowsyMin = reader["DrowsyMin"].ToString();
                    }
                    con.Close();
                }
            }
        }
    }
}